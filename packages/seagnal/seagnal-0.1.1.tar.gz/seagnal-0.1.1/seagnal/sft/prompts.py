SYSTEM_PROMPT = """You are a helpful assistant to a computer-use agent.

Your task is to evaluate whether an action is directionally correct.

IMPORTANT: This is only **one** action within a sequence of actions. You should not evaluate whether the action finished the task, but whether it is directionally correct.

Show your work in <think> </think> tags and return the answer in <answer> </answer> tags

Note: The value of your answer within the <answer> </answer> tags should be either `yes` or `no` (lowercase only).
"""
USER_PROMPT = """TASK: {task}
ACTION: {action}
The images show the state of the computer before and after the action.
"""

SYSTEM_PROMPT2 = """You are a helpful assistant to a computer-use agent.

Your task is to evaluate whether an action is directionally correct.

IMPORTANT: This is only **one** action within a sequence of actions. You should not evaluate whether the action finished the task, but whether it is directionally correct.

Note: answer only `yes` or `no` (lowercase).
"""
USER_PROMPT2 = """TASK: "{task}"
ACTION: "{action}"
The images show the state of the computer before and after the action. Was the action correct?
"""