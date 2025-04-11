import itertools

import manim as m
from manta.logger import log

from manta.components.shapes import ShapeUtils


class NeuralNetworkUtils(ShapeUtils):

    def simple_neural_network(self, input_layer_dim: int = 4,
                              hidden_layer_dim=4,
                              hidden_layer_n=2,
                              output_layer_dim=2,
                              neuron_circle_kwargs=None,
                              arrow_kwargs=None,
                              layer_horizontal_spacing: float = 1.0,
                              layer_vertical_spacing: float = 0.35) -> m.VGroup:

        if neuron_circle_kwargs is None:
            neuron_circle_kwargs = {}
        if arrow_kwargs is None:
            arrow_kwargs = {}

        default_neuron_circle_kwargs = {
            "radius": 0.1,
            "stroke_width": 2,
            "fill_color": self.background_color_bright,
            "stroke_color": self.outline_color,
            "fill_opacity": 0.0
        }
        merged_circle_kwargs = {**default_neuron_circle_kwargs, **neuron_circle_kwargs}

        default_connection_arrow_kwargs = {
            "stroke_width": 3 * 0.5,
            "buff": merged_circle_kwargs["radius"],
            "color": self.font_color,
            **arrow_kwargs
        }

        layers = []

        # input layer
        input_layer = m.VGroup()
        input_layer_center = m.ORIGIN
        input_layer_top_coord = input_layer_center + m.UP * (input_layer_dim - 1) * layer_vertical_spacing / 2
        for i in range(input_layer_dim):
            neuron = m.Circle(**merged_circle_kwargs)
            neuron.move_to(input_layer_top_coord)
            neuron.shift(i * m.DOWN * layer_vertical_spacing)
            input_layer.add(neuron)

        layers.append(input_layer)

        # hidden layers

        for idx_h_layer in range(hidden_layer_n):
            hidden_layer = m.VGroup()
            hidden_layer_center = m.ORIGIN + m.RIGHT * layer_horizontal_spacing * len(layers)
            hidden_layer_top_coord = hidden_layer_center + m.UP * (hidden_layer_dim - 1) * layer_vertical_spacing / 2
            for i in range(hidden_layer_dim):
                neuron = m.Circle(**merged_circle_kwargs)
                neuron.move_to(hidden_layer_top_coord)
                neuron.shift(i * m.DOWN * layer_vertical_spacing)
                hidden_layer.add(neuron)
            layers.append(hidden_layer)

        # output layer
        output_layer = m.VGroup()
        output_layer_center = m.ORIGIN + m.RIGHT * layer_horizontal_spacing * len(layers)
        output_layer_top_coord = output_layer_center + m.UP * (output_layer_dim - 1) * layer_vertical_spacing / 2

        for i in range(output_layer_dim):
            neuron = m.Circle(**merged_circle_kwargs)
            neuron.move_to(output_layer_top_coord)
            neuron.shift(i * m.DOWN * layer_vertical_spacing)
            output_layer.add(neuron)
        layers.append(output_layer)

        arrow_layers = []

        # connect layers
        for prev_layer, next_layer in zip(layers[:], layers[1:]):
            arrow_layer = m.VGroup()
            for prev_neuron in prev_layer:
                for next_neuron in next_layer:
                    arrow = m.Line(prev_neuron.get_center(), next_neuron.get_center(),
                                   **default_connection_arrow_kwargs)
                    arrow_layer.add(arrow)
            arrow_layers.append(arrow_layer)

        return m.VGroup(
            m.VGroup(*arrow_layers),
            m.VGroup(*layers),
        ).move_to(m.ORIGIN)

    def simple_neural_network_forward_animation(self, nn: m.VGroup, color: m.ManimColor | str = None,
                                                run_time=1.0) -> m.AnimationGroup:
        if color is None:
            color = self.magenta

        animations = []

        for layer_idx, (layer_connection, layer), in enumerate(zip(nn[0], nn[1])):
            layer_animation = m.AnimationGroup(
                m.Indicate(layer, color=color, scale_factor=1.0),
                m.ShowPassingFlash(layer_connection.copy().set_color(color), time_width=0.5),
                # I tried to introduce lag for each layer, the flow through the network looks much smoother to me
                # when I there is no stop between layers at all, so I set lag_ratio to 0.0
                # eventually this could be a parameter of the function, but for now I will leave it hardcoded
                lag_ratio=0.0,
            )
            animations.append(layer_animation)

        animations.append(
            m.Indicate(nn[1][-1], color=color, scale_factor=1.0, )
        )

        nn_animation = m.AnimationGroup(
            *animations,
            lag_ratio=0.5,
            run_time=run_time
        )

        return nn_animation

    def two_headed_network(self, shared_network_kwargs: dict = None,
                           shared_network_color: m.ManimColor | str = None,
                           top_head_network_kwargs: dict = None,
                           top_head_network_color: m.ManimColor | str = None,
                           bottom_networks_kwargs: dict = None,
                           bottom_networks_color: m.ManimColor | str = None,
                           connection_arrow_kwargs: dict = None,
                           layer_vertical_spacing=0.35,
                           layer_horizontal_spacing=1.0, ):

        if shared_network_kwargs is None:
            shared_network_kwargs = {}
        if top_head_network_kwargs is None:
            top_head_network_kwargs = {}
        if bottom_networks_kwargs is None:
            bottom_networks_kwargs = {}
        if connection_arrow_kwargs is None:
            connection_arrow_kwargs = {}

        if shared_network_color is None:
            shared_network_color = self.blue
        if top_head_network_color is None:
            top_head_network_color = self.green
        if bottom_networks_color is None:
            bottom_networks_color = self.magenta

        default_shared_network_kwargs = {
            "input_layer_dim": 8,
            "hidden_layer_dim": 7,
            "hidden_layer_n": 1,
            "output_layer_dim": 7,
            "neuron_circle_kwargs": {
                "radius": 0.1,
                "stroke_width": 2,
                "fill_color": self.background_color_bright,
                "stroke_color": shared_network_color,
                "fill_opacity": 0.0
            },
            "arrow_kwargs": None,
            "layer_horizontal_spacing": layer_horizontal_spacing,
            "layer_vertical_spacing": layer_vertical_spacing
        }
        default_top_head_network_kwargs = {
            "input_layer_dim": 3,
            "hidden_layer_dim": 3,
            "hidden_layer_n": 1,
            "output_layer_dim": 1,
            "neuron_circle_kwargs": {
                "radius": 0.1,
                "stroke_width": 2,
                "fill_color": self.background_color_bright,
                "stroke_color": top_head_network_color,
                "fill_opacity": 0.0
            },
            "arrow_kwargs": None,
            "layer_horizontal_spacing": layer_horizontal_spacing,
            "layer_vertical_spacing": layer_vertical_spacing
        }
        default_bottom_head_network_kwargs = {
            "input_layer_dim": 3,
            "hidden_layer_dim": 3,
            "hidden_layer_n": 1,
            "output_layer_dim": 2,
            "neuron_circle_kwargs": {
                "radius": 0.1,
                "stroke_width": 2,
                "fill_color": self.background_color_bright,
                "stroke_color": bottom_networks_color,
                "fill_opacity": 0.0
            },
            "arrow_kwargs": None,
            "layer_horizontal_spacing": layer_horizontal_spacing,
            "layer_vertical_spacing": layer_vertical_spacing
        }

        merged_shared_network_kwargs = {**default_shared_network_kwargs, **shared_network_kwargs}
        merged_top_head_network_kwargs = {**default_top_head_network_kwargs, **top_head_network_kwargs}
        merged_bottom_head_network_kwargs = {**default_bottom_head_network_kwargs, **bottom_networks_kwargs}

        top_nn = self.simple_neural_network(**merged_top_head_network_kwargs)
        bottom_nn = self.simple_neural_network(**merged_bottom_head_network_kwargs)

        bottom_nn.next_to(top_nn, m.DOWN, buff=layer_vertical_spacing)

        head_networks = m.VGroup(top_nn, bottom_nn)

        shared_nn = self.simple_neural_network(**merged_shared_network_kwargs)
        shared_nn.next_to(head_networks, m.LEFT, buff=layer_horizontal_spacing)

        _, shared_nn_layers = shared_nn
        _, top_nn_layers = top_nn
        _, bottom_nn_layers = bottom_nn

        input_layer = shared_nn_layers[0]
        output_layer_top = top_nn_layers[-1]
        output_layer_bottom = bottom_nn_layers[-1]

        output_layer = m.VGroup(output_layer_top, output_layer_bottom)

        default_connection_arrow_kwargs = {
            "stroke_width": 3 * 0.5,
            "buff": 0.1,
            "color": self.font_color
        }

        merged_connection_arrow_kwargs = {**default_connection_arrow_kwargs, **connection_arrow_kwargs}

        connection_arrows = m.VGroup()
        # connect last layer of shared network with first layer of top head network
        for shared_neuron in shared_nn_layers[-1]:
            for top_neuron in top_nn_layers[0]:
                arrow = m.Line(shared_neuron.get_center(), top_neuron.get_center(), **merged_connection_arrow_kwargs)
                connection_arrows.add(arrow)
        # connect ast layer of shared network with first layer of bottom head network
        for shared_neuron in shared_nn_layers[-1]:
            for bottom_neuron in bottom_nn_layers[0]:
                arrow = m.Line(shared_neuron.get_center(), bottom_neuron.get_center(), **merged_connection_arrow_kwargs)
                connection_arrows.add(arrow)

        # input_layer, output_layer, connection_arrows, shared_nn, top_nn, bottom_nn
        return m.VGroup(shared_nn, top_nn, bottom_nn, connection_arrows).move_to(
            m.ORIGIN
        )

    def two_headed_neural_network_forward_animation(self, two_headed_nn: m.VGroup, color: m.ManimColor | str = None,
                                                    run_time=1.5) -> m.AnimationGroup:
        if color is None:
            color = self.magenta

        try:
            shared_nn, top_nn, bottom_nn, connection_arrows = two_headed_nn
        except ValueError as e:
            log.warn("two_headed_nn should have 4 components: shared_nn, top_nn, bottom_nn, connection_arrows. "
                      "please check if you indeed passed a two_headed_nn to this function.")
            raise e

        shared_animation_group = self.simple_neural_network_forward_animation(shared_nn)
        top_animation_group = self.simple_neural_network_forward_animation(top_nn)
        bottom_animation_group = self.simple_neural_network_forward_animation(bottom_nn)

        animations = list(shared_animation_group.animations)

        animations.append(
            m.ShowPassingFlash(connection_arrows.copy().set_color(self.magenta), time_width=0.5),
        )

        for head_animations in itertools.zip_longest(top_animation_group.animations, bottom_animation_group.animations):
            animations.append(
                m.AnimationGroup(
                    # filter out None values
                    *[anim for anim in head_animations if anim is not None])
            )

        return m.AnimationGroup(
            *animations,
            lag_ratio=0.5,
            run_time=run_time
        )
