from typing import  Sequence, Union
import torch
import gradio as gr
from gradio.components import Component

from abc import abstractmethod, ABC

class ManifoldEndpoint(ABC):    
    
    def __init__(self, 
                name: str,
                description: str,
                url: str,
                inputs: Sequence[Union[str , Component]], 
                outputs: Sequence[Union[str , Component]],
                live: bool = False):
        self.name = name
        self.url = url
        self.description = description
        self.inputs = inputs
        self.outputs = outputs
        self.live = live
        self.default_variables = set(self.__dict__.keys())
        
    # ====================    
    # abstract method: user define function
    # ====================
    @abstractmethod
    def run(self, *args):
        """function for this endpoint"""
        pass
    
    def _run_main(self, *args):
        # yield self.run(*args)
        result = self.run(*args)
        return result
    
    # ====================    
    # gradio app
    # ====================
    def create_app(self):
        js_func = """
        function refresh() {
            const url = new URL(window.location);

            if (url.searchParams.get('__theme') !== 'light') {
                url.searchParams.set('__theme', 'light');
                window.location.href = url.href;
            }
        }
        """
        return gr.Interface(fn=self._run_main, 
                            inputs=self.inputs, 
                            outputs=self.outputs, 
                            # title=self.name, 
                            # description=self.description,
                            live=self.live,
                            theme=gr.themes.Base(primary_hue="slate",),
                            analytics_enabled=False,
                            css="footer{display:none !important} body{background-color: #000;}",   
                            js=js_func)

    # ====================    
    # handler method: trig by outside
    # ====================    
    def teardown_handler(self):
        """ Wrapper method that ensures teardown is followed by teardown check """
        try:
            self._teardown()  # Call teardown method which defined by user
        except Exception as e:
            raise e
    
    # ====================    
    # helper method
    # ====================
    def _teardown(self):
        """Delete variables added by user and move tensors/modules to CPU if needed."""
        current_variables = set(self.__dict__.keys())
        user_custom_variables = list(current_variables - self.default_variables)

        for v in user_custom_variables:
            attr = getattr(self, v, None)
            try:
                # If the attribute is a Tensor and on the GPU
                if isinstance(attr, torch.Tensor) and attr.is_cuda:
                    attr.cpu()  # Move the tensor to CPU
                    torch.cuda.synchronize()  # Ensure the move is complete
                    print(f"{self.url}: Moved tensor {v} from GPU to CPU")

                # If the attribute is an nn.Module (e.g., a model)
                elif isinstance(attr, torch.nn.Module):
                    attr.cpu()  # Move the model to CPU
                    torch.cuda.synchronize()  # Ensure the move is complete
                    print(f"{self.url}: Moved nn.Module {v} from GPU to CPU")

                # Delete the attribute after processing
                delattr(self, v)
                print(f"{self.url}: TearDown {v}")

            except Exception as e:
                print(f"Error during teardown for {v}: {str(e)}")
                raise Exception(f"Error during teardown for {v}: {str(e)}")

        # Empty cache after ensuring everything has been moved
        torch.cuda.empty_cache()
        print("GPU memory cache cleared.")
    
