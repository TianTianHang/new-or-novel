import numpy as np
import plotly.graph_objects as go
from scipy.signal import convolve2d


# def simulate_diffusion(num_particles, num_dimension, num_steps, step_size):
#     positions = np.zeros(shape=(num_particles, num_dimension))
#
#     for _ in range(num_steps):
#         positions += np.random.choice([-1, 1], size=(num_particles, num_dimension)) * step_size
#         yield positions
#
def generate_initial_values(x, y, n, max_value):
    initial_values = np.zeros((y, x))
    indices = np.random.choice(x * y, size=n, replace=False)
    initial_values.flat[indices] = np.random.uniform(low=max_value / 2, high=max_value, size=n)
    return initial_values


def heat_diffusion(x, y, num_steps, step_size):
    # 初始化数据
    positions = generate_initial_values(x, y, 500, 100)
    yield positions
    for _ in range(num_steps):
        # 构建扩散核
        diffusion_kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
        # 扩散过程
        laplacian = convolve2d(positions, diffusion_kernel, mode='same')
        positions += step_size * laplacian
        yield positions


def show_animate(x, y, num_steps, step_size):
    # 创建初始图形
    fig_dict = {"data": [], "frames": [], 'layout': dict(
        title='Diffusion Simulation',
        xaxis=dict(title='x_position'),
        yaxis=dict(title='y_position'),
        hovermode='closest',
    )}
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Step:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }
    # 添加初始数据点
    iter_diff = heat_diffusion(x, y, num_steps, step_size)
    inti_data = next(iter_diff)
    trace = go.Heatmap(x=np.arange(x), y=np.arange(y), z=inti_data)
    fig_dict['data'].append(trace)
    fig_dict['frames'].append(go.Frame(data=trace, name=str(1)))
    slider_step = {"args": [
        [1],
        {"frame": {"duration": 300, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": 1,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)
    # 创建帧
    for i, positions in enumerate(iter_diff):
        frame = go.Frame(
            data=go.Heatmap(x=np.arange(x), y=np.arange(y), z=positions), name=str(i + 2))
        fig_dict["frames"].append(frame)
        slider_step = {"args": [
            [i + 1],
            {"frame": {"duration": 300, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": 300}}
        ],
            "label": i + 1,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)

    # 创建按钮
    menu = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 300,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]
    fig_dict["layout"]['updatemenus'] = menu
    fig_dict["layout"]["sliders"] = [sliders_dict]
    fig = go.Figure(fig_dict)
    return fig


if __name__ == '__main__':
    # 模拟参数
    x = 100
    y = 100
    num_steps = 100
    step_size = 10
    fig = show_animate(x, y, num_steps, step_size)
    # 显示图形
    fig.show()
