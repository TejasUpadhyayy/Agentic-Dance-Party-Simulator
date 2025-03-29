# Agentic Dance Party Simulation

## P.S. I was SO tired of making useful projects and stuff for internships and academics. So made this on a whim, just something for fun. Enjoy. 

This is an advanced multi-agent system that models emergent social behaviors in a dance party environment. The simulation demonstrates complex social dynamics, relationship formation, and trend propagation through autonomous agents that respond to music and interact with each other.

## Features

- **Autonomous Dancing Agents:** Each dancer has unique personality traits (creativity, extroversion, rhythm sensitivity, etc.) that influence their behavior.
- **Dynamic Social Network Formation:** Dancers form relationships, dance groups, and conga lines based on compatibility and proximity.
- **Music Responsiveness:** Dancers react to beats and energy levels, either from real audio files or simulated music.
- **Emergent Trend Propagation:** Dance moves spread through the population based on social influence and visibility.
- **Interactive Control Panel:** Adjust simulation parameters in real-time and observe the effects.
- **Multiple Visual Themes:** Choose between different visual styles (Default, Neon, Pastel, Monochrome).
- **Camera Controls:** Zoom in/out and focus on specific dancers or areas.
- **Adjustable Dance Floor:** Change the size of the dance floor to create different crowd densities.

![dp1](https://github.com/user-attachments/assets/77ca6e16-f6d6-45a0-8e62-5ea904fc8d55)
![dp2](https://github.com/user-attachments/assets/8fcd910c-3d99-43c2-aac5-45acc07abc9f)
![dp3](https://github.com/user-attachments/assets/b2dea261-799e-40ad-971c-71e457858860)


## Technical Implementation

The simulation integrates several advanced computational models:

- **Personality Vector Representation:** Dancers exist in a multi-dimensional personality space.
- **Social Compatibility Metrics:** Relationships form based on weighted compatibility calculations.
- **Stochastic Decision Making:** Probabilistic behavior models create natural variability.
- **Group Formation Algorithms:** Spatial clustering with social cohesion analysis.
- **Trend Diffusion Models:** Modified epidemiological models for dance move propagation.
- **Real-time Audio Analysis:** Beat detection and energy extraction (when using audio files).

## Requirements

- Python 3.6+
- `pygame`
- `pygame_gui`
- `numpy`
- `tkinter` (for file dialogs)

## Installation

```sh
# Clone the repository
git clone https://github.com/yourusername/artificial-dance-party.git
cd artificial-dance-party

# Install requirements
pip install -r requirements.txt

# Run the simulation
python main.py
```

## Controls

- **Space:** Add a new dancer
- **R:** Randomize dancer positions
- **C:** Toggle control panel
- **M:** Change music file
- **ESC:** Quit

## Control Panel

The simulation includes an interactive control panel (toggle with 'C' key) with the following controls:

- **Music Tempo:** Adjust the BPM of the music
- **Dancer Creativity:** Change the creativity level of new dancers
- **Dancer Sociability:** Modify how social new dancers are
- **Dance Floor Size:** Adjust the dance area size
- **Group Formation Ease:** Control how easily dance groups form
- **Dance Floor Mood:** Set different mood environments (Normal, Energetic, Relaxed, Experimental)
- **Color Theme:** Change the visual theme of the simulation
- **Camera Controls:** Zoom in/out, focus on random dancers, reset view
- **Celebrity Dancer:** Add an influential dancer with high social impact
- **Change Music:** Select a different audio file
- **Reset Simulation:** Start over with fresh dancers

## Project Structure

```
artificial-dance-party/
│── main.py               # Entry point and main simulation loop
│── dancer.py             # Defines dancer agents and their behaviors
│── music_analyzer.py     # Handles audio analysis and beat detection
│── social_dynamics.py    # Manages social interactions between dancers
│── social_network.py     # Handles relationship formation and evolution
│── visualization.py      # Renders dancers and effects to the screen
│── control_panel.py      # Provides the interactive UI
```

## How It Works

At its core, the simulation operates on several interconnected systems:

- **Agent Cognition:** Each dancer makes decisions based on personality traits, current state, and environmental factors.
- **Social Dynamics:** Relationships form and evolve based on compatibility, shared experiences, and proximity.
- **Trend Propagation:** Dance moves spread through the population with trendsetters having greater influence.
- **Environmental Response:** The dance floor responds to music with reactive lighting and effects.

The complex interplay between these systems leads to emergent behaviors like distinct social groups, dance crazes, and spatial pattern formation - all without explicit programming of these higher-level phenomena.

## Extending the Simulation

The modular design allows for easy extension:

- Add new personality dimensions in `dancer.py`
- Implement additional social dynamics in `social_dynamics.py`
- Create new visual themes in `visualization.py`
- Add more control panel features in `control_panel.py`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The simulation draws inspiration from research in agent-based modeling, complex systems theory, and social network analysis.
- Audio analysis components are influenced by the music information retrieval community's approaches to beat detection.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

Enjoy the party! 🕺💃
