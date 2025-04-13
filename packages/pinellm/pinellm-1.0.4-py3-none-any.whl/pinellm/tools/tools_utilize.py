from ..schemas.safedot import SafeDotDict
from ..schemas.chat_request import Message, Content

def toolsutilize(return_model:SafeDotDict) -> list[Message]:
    """传入工具调用的返回模型"""
    from ..config.config_manager import ConfigManager
    config_manager = ConfigManager()
    tool_calls=return_model.choices.message.tool_calls
    if tool_calls:
        Messages = []
        function_name = tool_calls[0].function.name
        function_arguments = eval(tool_calls[0].function.arguments)
        try:
            function_return =  config_manager.Tools_Map[function_name](**function_arguments)
        except Exception as e:
            function_return = "工具调用失败，请检查参数是否正确"
        tool_calls=return_model.choices.message.tool_calls
        print(return_model.choices.message)
        Messages.append(Message(**return_model.choices.message.to_dict()))
        Messages.append(Message("tool", Content(text=f'{function_return}'), tool_call_id=return_model.choices.message.tool_calls.id))
        return Messages
    else:
        return []
        
        
    
    