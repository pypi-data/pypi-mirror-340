# Gymnasium CartPole SwingUp

[![PyPI version](https://badge.fury.io/py/gymnasium-cartpole-swingup.svg)](https://badge.fury.io/py/gymnasium-cartpole-swingup)
[![Python Versions](https://img.shields.io/pypi/pyversions/gymnasium-cartpole-swingup)](https://pypi.org/project/gymnasium-cartpole-swingup/)
[![License](https://img.shields.io/github/license/nkiyohara/gymnasium-cartpole-swingup)](https://github.com/nkiyohara/gymnasium-cartpole-swingup/blob/main/LICENSE)
[![Tests](https://github.com/nkiyohara/gymnasium-cartpole-swingup/actions/workflows/python-tests.yml/badge.svg)](https://github.com/nkiyohara/gymnasium-cartpole-swingup/actions/workflows/python-tests.yml)
[![GitHub release](https://img.shields.io/github/v/release/nkiyohara/gymnasium-cartpole-swingup)](https://github.com/nkiyohara/gymnasium-cartpole-swingup/releases)

A more challenging version of the classic CartPole environment for Gymnasium where the pole starts in a downward position.

## Description

This package provides a port of the CartPole SwingUp environment to the modern Gymnasium API. It is based on:
- [zuoxingdong/DeepPILCO](https://github.com/zuoxingdong/DeepPILCO/blob/master/cartpole_swingup.py)
- [hardmaru/estool](https://github.com/hardmaru/estool/blob/master/custom_envs/cartpole_swingup.py)

The environment has been updated to work with the latest Gymnasium interface and includes enhanced rendering capabilities.

## Installation

```bash
# Using pip
pip install gymnasium-cartpole-swingup

# Using uv
uv add gymnasium-cartpole-swingup
```

## Usage

```python
import gymnasium as gym
import gymnasium_cartpole_swingup  # This import is required to register the environment, even if unused

# Create the environment
env = gym.make("CartPoleSwingUp-v0", render_mode="human")
observation, info = env.reset(seed=42)

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    
    if terminated or truncated:
        observation, info = env.reset()

env.close()
```

### Customizing Environment Parameters

You can customize the physics parameters of the environment by passing them to `gym.make()`:

```python
# Create an environment with custom parameters
env = gym.make(
    "CartPoleSwingUp-v0",
    render_mode="human",
    gravity=9.81,             # Gravitational acceleration (m/s²)
    cart_mass=1.0,            # Mass of the cart (kg)
    pole_mass=0.1,            # Mass of the pole (kg)
    pole_length=0.6,          # Length of the pole (m)
    force_mag=10.0,           # Force magnitude scale applied to cart
    friction=0.05,            # Friction coefficient
    x_threshold=2.5,          # Cart position limit (left/right boundary)
    cost_mode="default",      # Cost function mode ("default" or "pilco")
    sigma_c=0.25,             # Sigma parameter for PILCO cost function
    obs_mode="raw",           # Observation mode ("raw" or "trig")
)
```

**Note**: The `import gymnasium_cartpole_swingup` line is necessary to register the environment with Gymnasium, even though it may appear unused. If you're using auto-formatters or linters that remove unused imports, you can add a `# noqa` comment or disable that specific check:

```python
import gymnasium_cartpole_swingup  # noqa: F401
```

## Environment Details

- **State**: Initially, the pole hangs downward ($\theta \approx \pi$)
- **Goal**: Swing the pole upright and maintain balance
- **Action Space**: Force applied to cart $[-1, 1]$ (scaled to $[-10, 10]$ N internally)
- **Observation Space**: Depends on the `obs_mode` parameter (see below)
- **Reward**: Higher when pole is upright and cart is centered

### Observation Space Detail

The environment supports two different observation space formats, which can be selected using the `obs_mode` parameter:

#### Raw Mode (`obs_mode="raw"`)

The default observation is a 4-dimensional vector:

| Index | Observation          | Description                            | Min  | Max  |
|-------|---------------------|----------------------------------------|------|------|
| 0     | $x$                 | Cart position along the track           | $-2.4$ | $2.4$  |
| 1     | $\dot{x}$           | Cart velocity                           | $-\infty$ | $\infty$ |
| 2     | $\theta$            | Angle of the pole                       | $-\pi$ | $\pi$  |
| 3     | $\dot{\theta}$      | Angular velocity of the pole            | $-\infty$ | $\infty$ |

#### Trigonometric Mode (`obs_mode="trig"`)

In this mode, the angle $\theta$ is replaced with its sine and cosine components, resulting in a 5-dimensional vector:

| Index | Observation          | Description                            | Min  | Max  |
|-------|---------------------|----------------------------------------|------|------|
| 0     | $x$                 | Cart position along the track           | $-2.4$ | $2.4$  |
| 1     | $\dot{x}$           | Cart velocity                           | $-\infty$ | $\infty$ |
| 2     | $\sin(\theta)$      | Sine of the pole angle                  | $-1.0$ | $1.0$  |
| 3     | $\cos(\theta)$      | Cosine of the pole angle                | $-1.0$ | $1.0$  |
| 4     | $\dot{\theta}$      | Angular velocity of the pole            | $-\infty$ | $\infty$ |

Using the trigonometric mode can be beneficial for learning algorithms as it provides a continuous representation of the angle without discontinuities at $\pm\pi$.

Notes:
- When the pole is upright, $\sin(\theta) = 0$ and $\cos(\theta) = 1$
- When the pole is hanging down, $\sin(\theta) = 0$ and $\cos(\theta) = -1$
- When the pole is horizontal to the right, $\sin(\theta) = 1$ and $\cos(\theta) = 0$
- When the pole is horizontal to the left, $\sin(\theta) = -1$ and $\cos(\theta) = 0$

For the raw mode:
- The angle $\theta$ is in radians and is kept within the range $[-\pi, \pi]$
- When the pole is upright, $\theta = 0$
- When the pole is hanging down, $\theta = \pi$ or $\theta = -\pi$

### Action Space Detail

The action is a 1-dimensional continuous value:

| Index | Action              | Description                            | Min  | Max  |
|-------|---------------------|----------------------------------------|------|------|
| 0     | $F$                 | Horizontal force applied to the cart   | $-1.0$ | $1.0$  |

Notes:
- The force is scaled internally by a factor of $10.0$, resulting in an effective range of $[-10, 10]$ N
- Positive values move the cart to the right
- Negative values move the cart to the left

### Reward Function

The environment supports two different reward (or cost) functions, which can be selected using the `cost_mode` parameter:

#### Default Mode (`cost_mode="default"`)

The default reward function is a product of two components:
- **Pole angle component**: $\cos(\theta)$
  - Maximum value of $1.0$ when the pole is upright ($\theta = 0$)
  - Minimum value of $-1.0$ when the pole is hanging down ($\theta = \pi$ or $\theta = -\pi$)

- **Cart position component**: $\cos(x)$
  - Maximum value of $1.0$ when the cart is centered ($x = 0$)
  - Decreases as the cart moves away from center

Total reward = pole angle component $\times$ cart position component

#### PILCO Mode (`cost_mode="pilco"`)

The PILCO (Probabilistic Inference for Learning COntrol) cost function is based on the squared distance between the pole tip position and the target position:

$cost = 1 - \exp(-\frac{d^2}{2\sigma_c^2})$

$reward = -cost$

Where:
- $d$ is the Euclidean distance between the current pole tip position and the target (upright) position
- $\sigma_c$ is a parameter controlling the width of the cost function (default: 0.25)

This cost function is more focused on the pole tip position in Cartesian space rather than the angular position and cart position separately.

### System Dynamics

The system dynamics follow the standard cart-pole physics model. The state update equations are:

$\ddot{x} = \frac{-2m_p l \dot{\theta}^2 \sin(\theta) + 3m_p g \sin(\theta)\cos(\theta) + 4F - 4b\dot{x}}{4(m_c + m_p) - 3m_p \cos^2(\theta)}$

$\ddot{\theta} = \frac{-3m_p l \dot{\theta}^2 \sin(\theta)\cos(\theta) + 6(m_c + m_p)g\sin(\theta) + 6(F - b\dot{x})\cos(\theta)}{4l(m_c + m_p) - 3m_p l \cos^2(\theta)}$

Where:
- $m_c = 0.5$ (kg): Mass of the cart (default)
- $m_p = 0.5$ (kg): Mass of the pole (default)
- $l = 0.6$ (m): Length of the pole (default)
- $g = 9.82$ (m/s²): Gravitational acceleration (default)
- $b = 0.1$: Friction coefficient (default)
- $F$: Applied force, scaled from action value to range $[-10, 10]$ N

All of these parameters can be customized when creating the environment as shown in the example above.
