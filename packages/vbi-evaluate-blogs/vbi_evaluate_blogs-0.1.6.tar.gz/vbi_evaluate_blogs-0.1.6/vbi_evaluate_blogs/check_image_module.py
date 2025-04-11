from langchain.schema import HumanMessage
from langchain.schema.messages import SystemMessage
from langchain_openai import AzureChatOpenAI
from langchain_community.chat_models import AzureChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from search_and_draw_module import get_base64_from_url

def describe_image(llm: AzureChatOpenAI, url: str) -> str:

    base64_image = get_base64_from_url(url)

    messages = [
        SystemMessage(content="You are an expert in analyzing images and text in documents."),
        HumanMessage(content=[
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            },
            {
                "type": "text",
                "text": (
                    "Please analyze the provided image in detail. "
                    "Describe the content, layout, colors, objects, text, and any other relevant features. "
                    "If the image contains text, extract and summarize it. "
                    "Provide a comprehensive and structured description."
                )
            }
        ])
    ]

    response = llm.invoke(messages)
    return response.content

def check_image(text_llm: AzureChatOpenAI,image_llm: AzureChatOpenAI, content: str) -> str:

    def describe_tool_func(image_url: str) -> str:
        base64_img = get_base64_from_url(image_url)
        if not base64_img:
            return f"Image at URL {image_url} is unavailable or could not be fetched."
        return describe_image(image_llm,image_url)

    tool = Tool(
        name="DescribeImage",
        func=describe_tool_func,
        description=(
            "Use this tool to analyze an image from a given URL. "
            "The tool will return layout, objects, and extracted text from the image."
        )
    )

    prompt = f"""
    <task>
        <role>
            You are a multi-modal reasoning assistant capable of deeply understanding both text and images. You can call tools to help analyze image content.
        </role>
        
        <goal>
            Your task is to go through a given document that includes images (in markdown or HTML form) and surrounding text.
            For each image, you must:
            1. Identify its URL and locate the nearest surrounding paragraph or context.
            2. Use the tool <tool>DescribeImage</tool> to analyze the image if needed.
            3. Evaluate whether the image is relevant and supportive to the nearby text context.
            4. Return a structured, numbered report of your findings for each image.
        </goal>

        <constraints>
            - Only analyze actual image URLs (e.g., ending with .jpg, .png, .jpeg, .webp).
            - Ignore logos, icons, or purely decorative images unless they have textual importance.
            - Use DescribeImage tool only when image relevance is unclear or important to justify.
            - Your response should be in concise markdown format with clear, structured feedback.

        </constraints>

        <output_format>
            <Feild>Return result in Markdown format.</Feild>
            - For each image:
                - Image #: [index]
                - Image URL: [url]
                - Description: [summary if DescribeImage used]
                - Text Context: [quoted or summarized nearby text]
                - Assessment: [Does it support the text? Yes/No. Justification.]
        </output_format>

        <final_instruction>
            Do not fabricate image content. If an image fails to load, mark it as [unavailable].
        </final_instruction>
    </task>

    <document>
    {content}
    </document>
    """

    # Khởi tạo agent
    agent = initialize_agent(
        tools=[tool],
        llm=text_llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        
    )

    return agent.invoke(prompt.strip())['output']

if __name__ == "__main__":
    from langchain_openai import AzureChatOpenAI
    from dotenv import load_dotenv
    import os
    from extract_module import extract_image

    load_dotenv()

    image_llm = AzureChatOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            model="gpt-4o-mini",
            api_version="2024-08-01-preview",
            temperature=0.7,
            max_tokens=16000
        )

    text_llm = AzureChatOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            model="o3-mini",
            api_version="2024-12-01-preview",
        )
    
    content = """
![](https://statics.gemxresearch.com/images/2025/04/09/160400/a-3d-render-of-a-pixar-style-cyberpunk-c_MgA2jR6QRoG4LMg9Y1m1Sw_ACcWep5XRhmU2SRVMLuXpg.jpeg)
 
# Doanh thu của nền tảng Virtuals Protocol sụt giảm mạnh xuống mức thấp kỷ lục 500 USD/ngày
 
Nền tảng tạo và kiếm tiền từ AI agent Virtuals Protocol đã chứng kiến doanh thu hàng ngày giảm mạnh xuống chỉ còn 500 USD khi nhu cầu về AI agent tiếp tục suy giảm."Có lẽ đây là một trong những biểu đồ  điên rồ nhất của chu kỳ này," nhà nghiên cứu Blockworks Sharples đã chia sẻ trong bài đăng trên X vào ngày 8 tháng 4. [Twitter Post](https://twitter.com/0xSharples/status/1909597333706232109) 
## Sự sụt giảm mạnh trong việc tạo AI agent
 
Sharples cho biết đã "khoảng một tuần" kể từ khi một đại lý AI mới được ra mắt trên Virtuals, so với cuối tháng 11 khi nền tảng này đang giúp tạo ra hơn 1.000 đại lý AI mới mỗi ngày, theo dữ liệu từ Dune Analytics.Vào ngày 2 tháng 1, khi token của Virtual Protocol (VIRTUAL) đạt mức cao kỷ lục 4,61 USD, dữ liệu của Blockworks cho thấy doanh thu hàng ngày của Virtuals đã tăng vọt lên trên 500.000 USD.Tuy nhiên, thời điểm đó dường như đánh dấu sự bắt đầu của xu hướng giảm, báo hiệu một đỉnh tiềm năng cho lĩnh vực đại lý AI. Sự suy giảm tiếp tục diễn ra ngay cả sau thông báo vào ngày 25 tháng 1 rằng dự án đã mở rộng sang Solana.Vào ngày 7 tháng 4, Sharples chỉ ra rằng Virtuals tạo ra "chưa đến 500 USD" doanh thu hàng ngày, với giá token giảm xuống mức thấp nhất là 0,42 USD.![](https://statics.gemxresearch.com/images/2025/04/09/154952/0196188f-6f21-7965-8e50-3a700d29.jpg)  Trước đó,[ Virtual đã có động thái mở rộng sang Solana](https://gfiresearch.net/post/virtuals-mo-rong-sang-he-sinh-thai-solana-thiet-lap-quy-du-tru-sol-chien-luoc) nhưng tình hình vẫn không mấy khả quan. 
## Tổng giá trị thị trường AI agent
 
Tổng giá trị thị trường đại lý AI là 153,81 triệu USD, theo Dune Analytics. Tuy nhiên, 76,6 triệu USD trong số đó được phân bổ cho AIXBT, công cụ phân tích tâm lý tiền mã hóa trên mạng xã hội X để nắm bắt xu hướng.AIXBT đã giảm 92% kể từ khi đạt mức cao kỷ lục 0,90 USD vào ngày 16 tháng 1. Tại thời điểm xuất bản, nó đang được giao dịch ở mức 0,07 USD, theo dữ liệu của CoinMarketCap.![](https://statics.gemxresearch.com/images/2025/04/09/155134/image.png)  Cộng tác viên chính của DeGen Capital, Mardo cho biết điều kiện thị trường hiện tại đã đóng vai trò trong sự suy giảm của Virtuals, nhưng nó cũng có thể liên quan đến các điều khoản mà Virtuals có với các nhà phát triển, chẳng hạn như "giữ lại thuế token mà các nền tảng khác tự do hoàn trả."Những khó khăn của Virtuals xảy ra trong bối cảnh toàn bộ thị trường tiền điện tử đang trải qua sự suy thoái cùng với thị trường tài chính toàn cầu, khi Tổng thống Hoa Kỳ Donald Trump tiếp tục tăng thuế quan và nỗi lo ngại gia tăng rằng điều đó có thể dẫn đến suy thoái kinh tế. 
## AI agent hiện tại bị đánh giá là "vô giá trị"
 
Tuy nhiên, nhiều người chỉ trích các đại lý AI vì thiếu chức năng. Nhà bình luận AI, BitDuke đã nói về sự suy giảm doanh thu của Virtuals: "Những kẻ ăn theo ChatGPT không còn thú vị nữa, dễ đoán mà."Nhà bình luận AI "DHH" đã nói trong bài đăng trên X vào ngày 8 tháng 4: "Tôi cũng tích cực về AI, nhưng bạn thật ảo tưởng nếu nghĩ rằng bất kỳ AI agent nào sẽ hoàn toàn thay thế một lập trình viên giỏi ngày nay. Ai biết về ngày mai, nhưng ngày đó chưa đến."Trong khi đó, người sáng lập Infinex Kain Warwick gần đây đã nói với tạp chí rằng AI có thể trở lại mặc dù "phiên bản đầu tiên của các AI agent lộn xộn" bị coi là "vô giá trị."
"""

    print(check_image(text_llm,image_llm,content))