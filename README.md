# Python Tetris

A classic implementation of Tetris using Python and Pygame. This game features all the standard Tetris mechanics along with modern features like ghost pieces and a next-piece preview.

![Tetris Game Screenshot](screenshots/tetris.png)

## Features

- Classic Tetris gameplay mechanics
- Ghost piece preview showing where pieces will land
- Next piece preview
- Score tracking and level progression
- Increasing difficulty as levels progress
- Clean, modern visual design
- AI Bot that can play the game automatically

## Requirements

- Python 3.7+
- Pygame 2.5.2
- NumPy 1.24.3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aarav-paul/python-tetris.git
cd python-tetris
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

### Manual Play
Run the game using:
```bash
python tetris.py
```

### AI Bot Play
Watch the AI bot play automatically:
```bash
python tetris_bot.py
```

### Controls

- **Left Arrow**: Move piece left
- **Right Arrow**: Move piece right
- **Up Arrow**: Rotate piece
- **Down Arrow**: Soft drop (move piece down faster)
- **Spacebar**: Hard drop (instantly drop piece)

### Scoring

- Points are awarded for clearing lines
- Clearing multiple lines at once gives bonus points
- The game speeds up as your score increases
- Each level increases the falling speed of the pieces

## AI Bot Details

The game includes an AI bot that can play automatically. The bot uses a heuristic-based approach to make decisions, evaluating positions based on:

- Number of holes (empty spaces with blocks above)
- Surface bumpiness (difference in heights between adjacent columns)
- Total stack height
- Number of complete lines

The bot's decision-making process:
1. For each piece, it simulates all possible:
   - Rotations (0°, 90°, 180°, 270°)
   - Horizontal positions
   - Landing positions
2. Evaluates each possible position using weighted metrics
3. Chooses the move that maximizes the overall score

You can watch the bot play by running `python tetris_bot.py`. The bot will automatically make moves until it loses.

## Project Structure

```
python-tetris/
├── tetris.py          # Main game file
├── tetris_bot.py      # AI bot implementation
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Contributing

Feel free to fork this project and submit pull requests with improvements. Some ideas for contributions:

- Add sound effects
- Implement high score tracking
- Add different game modes
- Improve visual effects
- Enhance the AI bot's strategy
- Add machine learning to optimize bot performance

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original Tetris game design by Alexey Pajitnov
- Built with [Pygame](https://www.pygame.org/) 