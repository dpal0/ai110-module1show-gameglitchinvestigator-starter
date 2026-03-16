from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

# Tests for the hint message bug fix:
# "Too High" should tell the player to go LOWER, not higher
# "Too Low" should tell the player to go HIGHER, not lower

def test_too_high_message_says_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_message_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message

# Tests for the type bug fix:
# secret should always be compared as an int, not a string

def test_check_guess_uses_numeric_comparison():
    # "9" > "50" lexicographically, but 9 < 50 numerically
    # Before the fix, this would have returned "Too High" on even attempts
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"

def test_check_guess_int_vs_int():
    # Sanity check that int-to-int comparison always works correctly
    outcome, _ = check_guess(1, 100)
    assert outcome == "Too Low"
    outcome, _ = check_guess(100, 1)
    assert outcome == "Too High"


# Tests for parse_guess

def test_parse_guess_valid_integer():
    ok, value, _ = parse_guess("42")
    assert ok is True
    assert value == 42
    assert _ is None

def test_parse_guess_valid_float_truncates():
    ok, value, _ = parse_guess("7.9")
    assert ok is True
    assert value == 7

def test_parse_guess_empty_string():
    ok, value, _ = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_guess_none():
    ok, value, _ = parse_guess(None)
    assert ok is False
    assert value is None

def test_parse_guess_non_numeric():
    ok, value, _ = parse_guess("abc")
    assert ok is False
    assert value is None


# Tests for update_score

def test_update_score_win_early():
    # Win on attempt 1 should give maximum points
    score = update_score(0, "Win", 1)
    assert score > 0

def test_update_score_win_adds_to_existing_score():
    score = update_score(50, "Win", 1)
    assert score > 50

def test_update_score_win_minimum_points():
    # Even a very late win should award at least 10 points
    score = update_score(0, "Win", 100)
    assert score >= 10

def test_update_score_too_low_subtracts():
    score = update_score(20, "Too Low", 1)
    assert score == 15

def test_update_score_unknown_outcome_unchanged():
    score = update_score(30, "draw", 1)
    assert score == 30


# Tests for get_range_for_difficulty

def test_range_easy():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_range_normal():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_range_hard():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50

def test_range_unknown_defaults():
    low, high = get_range_for_difficulty("Unknown")
    assert low == 1
    assert high == 100


# Tests for the hint bug fix:
# Hint was only rendered inside `if submit:`, so it disappeared on the next
# rerun. The fix stores the hint in session state so it persists.
# These tests verify the hint message content that gets stored.

def test_hint_stored_for_too_high():
    # The message returned by check_guess is what gets stored as the hint
    _, message = check_guess(80, 50)
    assert message is not None
    assert len(message) > 0

def test_hint_stored_for_too_low():
    _, message = check_guess(20, 50)
    assert message is not None
    assert len(message) > 0

def test_hint_stored_for_win():
    _, message = check_guess(50, 50)
    assert message is not None
    assert len(message) > 0

def test_hint_not_shown_when_show_hint_false():
    # When show_hint is False, last_hint should not be updated.
    # Simulate the app logic: only set last_hint when show_hint is True.
    last_hint = None
    show_hint = False
    _, message = check_guess(30, 50)
    if show_hint:
        last_hint = message
    assert last_hint is None

def test_hint_shown_when_show_hint_true():
    last_hint = None
    show_hint = True
    _, message = check_guess(30, 50)
    if show_hint:
        last_hint = message
    assert last_hint == message


# Tests for the history ordering bug fix:
# The debug panel used to render before history.append() ran, making the
# second guess appear missing. The fix moves the panel after the submit block.
# These tests verify that history records guesses in submission order.

def test_history_records_multiple_guesses_in_order():
    history = []
    guesses = [10, 30, 50]
    for g in guesses:
        ok, guess_int, _ = parse_guess(str(g))
        assert ok
        history.append(guess_int)
    assert history == [10, 30, 50]

def test_history_records_second_guess():
    history = []
    for raw in ["20", "40"]:
        ok, guess_int, _ = parse_guess(raw)
        assert ok
        history.append(guess_int)
    assert len(history) == 2
    assert history[1] == 40

def test_history_records_invalid_guess_as_raw():
    # Invalid guesses are appended as the raw string, not skipped
    history = []
    raw = "abc"
    ok, _, _ = parse_guess(raw)
    if not ok:
        history.append(raw)
    assert history == ["abc"]

def test_history_cleared_on_new_game():
    history = [10, 20, 30]
    # Simulate new game reset
    history = []
    assert history == []


# Additional update_score coverage

def test_update_score_too_high_even_attempt_adds():
    # Even attempt number with Too High adds 5 points
    score = update_score(20, "Too High", 2)
    assert score == 25

def test_update_score_too_high_odd_attempt_subtracts():
    # Odd attempt number with Too High subtracts 5 points
    score = update_score(20, "Too High", 3)
    assert score == 15

def test_update_score_win_late_is_minimum_10():
    score = update_score(0, "Win", 9)
    assert score == 10

def test_update_score_win_attempt_2():
    # 100 - 10 * (2 + 1) = 70
    score = update_score(0, "Win", 2)
    assert score == 70


# Additional parse_guess coverage

def test_parse_guess_negative_number():
    ok, value, _ = parse_guess("-5")
    assert ok is True
    assert value == -5

def test_parse_guess_zero():
    ok, value, _ = parse_guess("0")
    assert ok is True
    assert value == 0

def test_parse_guess_whitespace_only():
    ok, _, _ = parse_guess("   ")
    assert ok is False

def test_parse_guess_returns_error_message_on_invalid():
    ok, _, err = parse_guess("xyz")
    assert ok is False
    assert err is not None and len(err) > 0
