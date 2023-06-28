import openai
import os
import json

class AI:
    def __init__(self, chatgpt_api_key, mode='gpt', cache=True):
        self.chatgpt_api_key = chatgpt_api_key
        self.mode = mode
        self.generated_code_cache = {}
        self.cache_file = "code_cache.json"
        self.cache = cache
        if cache:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, "r") as f:
                    self.generated_code_cache = json.load(f)

    def __getattr__(self, method_name):
        def method(*args, **kwargs):
            if method_name in self.generated_code_cache:
                generated_code = self.generated_code_cache[method_name]
                print("代码从缓存中获取")
                
            else:
                generated_code = self.call_chatgpt(method_name, *args, **kwargs)
                print("首次生成的代码")

            print('#################code#################')
            print(generated_code)
            print('######################################')

            try:
                exec(generated_code, globals())
                result = eval(f"{method_name}(*args, **kwargs)")
                print('函数输出：',result,'\n\n')
                if self.cache:
                    if method_name not in self.generated_code_cache:
                        self.generated_code_cache[method_name] = generated_code
                        with open(self.cache_file, "w") as f:
                            json.dump(self.generated_code_cache, f)
                return result
            except Exception as e:
                print(f"生成或执行代码时出错: {e}")
                return None
            

        return method

    def call_chatgpt(self, method_name, *args, **kwargs):
        prompt = f"你是一个乐于助人的python专家，擅长编写各种python函数。\
        请帮我编写一个Python函数，函数命名为<{method_name}>，\
        你不可以对函数名做任何改动！传入的参数示例为：*{args}。\
        请给每个参数都设置一个默认参数。保证用户传参和函数要求一致。\
        导包务必放到函数内,注意导入所有所需的包。\
        请根据函数名和参数示例推理并实现该函数，不能用pass敷衍！\
        函数的结果必须要<return出来>而不是print\
        不需要测试！要求只输出代码，无需任何解释"
        openai.api_key = self.chatgpt_api_key

        if self.mode == 'davinci':
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.5,
            )
            return response.choices[0].text.replace('。','').replace('！','').replace('```python','').replace('```','').strip()

        if self.mode == 'gpt':
            try:
                response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=eval('[{"role":"user", "content":"' + prompt + '"}]'),
                    temperature=0
                )
                assistant_response = response.choices[0].message['content']
                return assistant_response.replace('```python','').replace('```','').strip()
            except Exception as e:
                print(f"生成或执行代码时出错: {e}")
                response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.5,
                )
                return response.choices[0].text.replace('。','').replace('！','').replace('```python','').replace('```','').strip()

if __name__ == '__main__':
    # 测试用例
    ai = AI("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")
    ai.plot绘制柱状图([2,3])
    ai.plot绘制柱状图([2,3,7])
