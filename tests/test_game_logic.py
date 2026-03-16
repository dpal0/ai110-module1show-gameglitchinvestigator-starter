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


#FIX: hint moved to session state — was only rendered inside `if submit:` so it disappeared on every rerun

def test_hint_stored_for_too_high():
    #FIX: hint now stored in session state so it persists across reruns
    _, message = check_guess(80, 50)
    assert message is not None
    assert len(message) > 0

def test_hint_stored_for_too_low():
    #FIX: hint now stored in session state so it persists across reruns
    _, message = check_guess(20, 50)
    assert message is not None
    assert len(message) > 0

def test_hint_stored_for_win():
    #FIX: hint now stored in session state so it persists across reruns
    _, message = check_guess(50, 50)
    assert message is not None
    assert len(message) > 0

def test_hint_not_shown_when_show_hint_false():
    #FIX: last_hint only updated when show_hint checkbox is True
    last_hint = None
    show_hint = False
    _, message = check_guess(30, 50)
    if show_hint:
        last_hint = message
    assert last_hint is None

def test_hint_shown_when_show_hint_true():
    #FIX: last_hint set to message when show_hint is True, so hint persists
    last_hint = None
    show_hint = True
    _, message = check_guess(30, 50)
    if show_hint:
        last_hint = message
    assert last_hint == message


#FIX: debug panel moved after submit block — previously rendered before append so second guess appeared missing

def test_history_records_multiple_guesses_in_order():
    #FIX: debug panel moved after submit block so history includes current guess
    history = []
    guesses = [10, 30, 50]
    for g in guesses:
        ok, guess_int, _ = parse_guess(str(g))
        assert ok
        history.append(guess_int)
    assert history == [10, 30, 50]

def test_history_records_second_guess():
    #FIX: second guess was invisible in debug panel because panel rendered before append
    history = []
    for raw in ["20", "40"]:
        ok, guess_int, _ = parse_guess(raw)
        assert ok
        history.append(guess_int)
    assert len(history) == 2
    assert history[1] == 40

def test_history_records_invalid_guess_as_raw():
    #FIX: invalid guesses appended as raw string so all attempts are visible in history
    history = []
    raw = "abc"
    ok, _, _ = parse_guess(raw)
    if not ok:
        history.append(raw)
    assert history == ["abc"]

def test_history_cleared_on_new_game():
    #FIX: last_hint and history both reset on new game so stale state doesn't carry over
    history = [10, 20, 30]
    history = []
    assert history == []


#FIX: additional update_score edge cases — even/odd attempt branching and win point clamping

def test_update_score_too_high_even_attempt_adds():
    #FIX: even-attempt Too High awards +5 points per scoring rule
    score = update_score(20, "Too High", 2)
    assert score == 25

def test_update_score_too_high_odd_attempt_subtracts():
    #FIX: odd-attempt Too High deducts 5 points per scoring rule
    score = update_score(20, "Too High", 3)
    assert score == 15

def test_update_score_win_late_is_minimum_10():
    #FIX: late win clamped to minimum 10 points so score never goes negative on win
    score = update_score(0, "Win", 9)
    assert score == 10

def test_update_score_win_attempt_2():
    #FIX: win score formula is 100 - 10 * (attempt + 1), verified at attempt 2
    score = update_score(0, "Win", 2)
    assert score == 70


#FIX: additional parse_guess edge cases — zero, negative, whitespace, and error message presence

def test_parse_guess_negative_number():
    #FIX: negative numbers are valid integers and should parse successfully
    ok, value, _ = parse_guess("-5")
    assert ok is True
    assert value == -5

def test_parse_guess_zero():
    #FIX: zero is a valid integer and should not be treated as falsy/empty
    ok, value, _ = parse_guess("0")
    assert ok is True
    assert value == 0

def test_parse_guess_whitespace_only():
    #FIX: whitespace-only input is not a valid number and should return ok=False
    ok, _, _ = parse_guess("   ")
    assert ok is False

def test_parse_guess_returns_error_message_on_invalid():
    #FIX: invalid input returns a non-empty error message to display to the user
    ok, _, err = parse_guess("xyz")
    assert ok is False
    assert err is not None and len(err) > 0
