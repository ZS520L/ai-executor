import openai
import os
import json

class AI:
    def __init__(self, chatgpt_api_key, mode='gpt'):
        self.chatgpt_api_key = chatgpt_api_key
        self.mode = mode
        self.generated_code_cache = {}
        self.cache_file = "code_cache.json"

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
            print('\n################result################')

            try:
                exec(generated_code, globals())
                print('\n\n\n')

                if method_name not in self.generated_code_cache:
                    self.generated_code_cache[method_name] = generated_code
                    with open(self.cache_file, "w") as f:
                        json.dump(self.generated_code_cache, f)

            except Exception as e:
                print(f"执行生成代码时出错: {e}")
                return None

        return method

    def call_chatgpt(self, method_name, *args, **kwargs):
        # prompt = f"编写一个Python函数，名为{method_name}，接受以下参数：{args} {kwargs}。请根据函数名推理并实现该函数，并在最后增加函数调用代码。注意：只输出函数代码，不要包含其他无关信息。"
        prompt = f"编写一个Python函数，名为{method_name}，接受以下参数：{args} {kwargs}，请根据函数名推理并实现该函数，并在最后增加函数调用代码。要求只输出代码，无需任何解释"
        
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
            return response.choices[0].text.strip()

        if self.mode == 'gpt':
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=eval('[{"role":"user", "content":"' + prompt + '"}]'),
                temperature=0
            )
            assistant_response = response.choices[0].message['content']
            return assistant_response.replace('```python','').replace('```','').strip()
if __name__ == '__main__':
    # 用例
    ai = AI("sk-4mqNlIS3Fi4XWPoz3o6mT36378FJKVCt1NGvbFOT547L2Jv7")
    ai.a_add_b(3, 4)
    ai.a的b次幂(3, 4)
    ai.绘制折线图([1,3,4,5,7,6,3,8])
    ai.使用plot读取图片二值化后可视化('/content/4.png')
