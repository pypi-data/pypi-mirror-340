, filename))
        plt.close()
    
    def _visualize_cnn(self, architecture: Tuple[List[Dict[str, Any]], List[int]], filename: str) -> None:
        """Visualize CNN architecture"""
        conv_layers, fc_layers = architecture
        
        # Create figure with two subplots - one for the overall architecture, one for details
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [1, 2]})
        
        # Top subplot: Overall architecture diagram
        layer_types = ['Input'] + ['Conv'] * len(conv_layers) + ['FC'] * len(fc_layers)
        layer_names = ['Input']
        
        # Add conv layer names
        for i, layer in enumerate(conv_layers):
            filters = layer.get('filters', 0)
            kernel = layer.get('kernel_size', 3)
            layer_names.append(f"Conv\n{filters}@{kernel}x{kernel}")
        
        # Add fc layer names
        for neurons in fc_layers:
            layer_names.append(f"FC\n{neurons}")
        
        # Draw boxes for each layer
        n_layers = len(layer_names)
        box_width = 0.8
        box_spacing = 1.2
        
        for i, (name, layer_type) in enumerate(zip(layer_names, layer_types)):
            # Position
            x = i * box_spacing
            y = 0
            
            # Color based on layer type
            if layer_type == 'Input':
                color = 'lightgreen'
            elif layer_type == 'Conv':
                color = 'lightblue'
            else:  # FC
                color = 'lightcoral'
            
            # Draw box
            rect = plt.Rectangle((x - box_width/2, y - 0.5), box_width, 1, 
                                 fill=True, color=color, zorder=3)
            ax1.add_patch(rect)
            
            # Add text
            ax1.text(x, y, name, ha='center', va='center', zorder=4)
            
            # Draw arrows
            if i < n_layers - 1:
                ax1.arrow(x + box_width/2, y, box_spacing - box_width, 0, 
                         head_width=0.1, head_length=0.1, fc='black', ec='black', zorder=2)
        
        # Set limits and turn off axis
        ax1.set_xlim(-1, (n_layers - 1) * box_spacing + 1)
        ax1.set_ylim(-1, 1)
        ax1.axis('off')
        ax1.set_title("CNN Architecture Overview")
        
        # Bottom subplot: Detailed architecture information
        # Create table data
        table_data = [
            ["Layer", "Type", "Output Shape", "Parameters"]
        ]
        
        # Add input layer
        input_shape = (3, 32, 32)  # Placeholder, should be replaced with actual shape
        table_data.append(["Input", "Input", str(input_shape), "0"])
        
        # Track current shape
        c, h, w = input_shape
        param_count = 0
        
        # Add conv layers
        for i, layer in enumerate(conv_layers):
            filters = layer.get('filters', 0)
            kernel = layer.get('kernel_size', 3)
            padding = layer.get('padding', 0)
            stride = layer.get('stride', 1)
            pool_size = layer.get('pool_size', 1)
            
            # Calculate output shape after conv
            h_out = (h - kernel + 2 * padding) // stride + 1
            w_out = (w - kernel + 2 * padding) // stride + 1
            
            # Calculate parameters
            params = filters * (c * kernel * kernel + 1)  # +1 for bias
            param_count += params
            
            # Add to table
            output_shape = f"({filters}, {h_out}, {w_out})"
            table_data.append([f"Conv{i+1}", f"{kernel}x{kernel} Conv", output_shape, f"{params:,}"])
            
            # Update shape for next layer
            c, h, w = filters, h_out, w_out
            
            # Add pooling if applicable
            if pool_size > 1:
                h_out = h // pool_size
                w_out = w // pool_size
                
                output_shape = f"({c}, {h_out}, {w_out})"
                table_data.append([f"Pool{i+1}", f"{pool_size}x{pool_size} MaxPool", output_shape, "0"])
                
                # Update shape for next layer
                h, w = h_out, w_out
        
        # Add flatten layer
        flattened_size = c * h * w
        table_data.append(["Flatten", "Flatten", f"({flattened_size})", "0"])
        
        # Add fully connected layers
        fc_input_size = flattened_size
        for i, neurons in enumerate(fc_layers):
            # Calculate parameters
            params = fc_input_size * neurons + neurons  # weights + biases
            param_count += params
            
            # Add to table
            table_data.append([f"FC{i+1}", "Fully Connected", f"({neurons})", f"{params:,}"])
            
            # Update shape for next layer
            fc_input_size = neurons
        
        # Add total row
        table_data.append(["Total", "", "", f"{param_count:,}"])
        
        # Create table
        ax2.axis('tight')
        ax2.axis('off')
        
        table = ax2.table(cellText=table_data[1:], 
                         colLabels=table_data[0], 
                         loc='center',
                         cellLoc='center')
        
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
        
        ax2.set_title("CNN Architecture Details")
        
        # Adjust layout and save
        plt.tight_layout()
        plt.savefig(os.path.join(self.log_dir, filename))
        plt.close()
