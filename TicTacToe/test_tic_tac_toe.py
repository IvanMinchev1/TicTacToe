import unittest
from MinimaxTicTacToe import TicTacToe  

class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe()

    def test_initial_board_setup(self):
        """Test that the board is initialized correctly."""
        expected_board = {i: ' ' for i in range(1, 10)}
        self.assertEqual(self.game.board, expected_board)

    def test_move_making(self):
        """Test making moves on the board."""
        self.game.update_player_position('X', 1)
        self.assertEqual(self.game.board[1], 'X')
        self.assertTrue(self.game.update_player_position('O', 2))
        self.assertEqual(self.game.board[2], 'O')
        self.assertFalse(self.game.update_player_position('X', 2))

    def test_win_condition(self):
        """Test win conditions for the game."""
        # Horizontal win
        for i in range(1, 4):
            self.game.board[i] = 'X'
        self.assertTrue(self.game.is_winning('X'))

        self.setUp()  # Reset the game for a new test scenario

        # Vertical win
        for i in range(1, 8, 3):
            self.game.board[i] = 'O'
        self.assertTrue(self.game.is_winning('O'))

        self.setUp()  # Reset the game for a new test scenario

        # Diagonal win
        self.game.board[1] = self.game.board[5] = self.game.board[9] = 'X'
        self.assertTrue(self.game.is_winning('X'))

    def test_draw_condition(self):
        """Test the draw condition."""
        moves = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X']
        for i, move in enumerate(moves, start=1):
            self.game.board[i] = move
        self.assertTrue(self.game.is_draw())

    def test_switch_player(self):
        """Test switching the current player."""
        self.assertEqual(self.game.current_player, 'O')
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 'X')
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 'O')

    def test_reset_game(self):
        """Test resetting the game to its initial state."""
        # Make some moves
        self.game.update_player_position('X', 1)
        self.game.update_player_position('O', 2)
        # Reset the game
        self.game.reset_game()
        expected_board = {i: ' ' for i in range(1, 10)}
        self.assertEqual(self.game.board, expected_board)
        self.assertEqual(self.game.current_player, 'O')


if __name__ == '__main__':
    unittest.main()
