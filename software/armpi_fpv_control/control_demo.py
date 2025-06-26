from ros_robot_controller_sdk import Board
from action_group_controller import ActionGroupController

controller = ActionGroupController(Board())
# 动作组需要保存在当前路径的ActionGroups下(action group need to be saved in current path "ActionGroups")
controller.runAction('wave') # 参数为动作组的名称，不包含后缀，以字符形式传入(parameter is the name of action group, the suffix is not included, inform as character form)
