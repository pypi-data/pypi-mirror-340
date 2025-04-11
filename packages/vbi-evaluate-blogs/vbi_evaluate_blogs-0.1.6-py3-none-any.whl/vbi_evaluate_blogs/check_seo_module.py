from langchain_openai import AzureChatOpenAI

def check_keyword_distribution(llm: AzureChatOpenAI, text: str) -> str:  
    """Check keyword distribution in the article."""  
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>SEO expert</strong> with proven experience in optimizing content for high performance on search engines like Google and Bing.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>evaluate the keyword usage and distribution</strong> in a given article, ensuring SEO optimization while avoiding keyword stuffing.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Identify and Analyze Main Keywords</Title>
                    <Details>
                        <Point>Check if the main keywords appear in the title, H1 heading, and meta description (or introductory paragraph if no meta is available).</Point>
                        <Point>Check if the main keywords appear in the first 100 words of the content.</Point>
                        <Point>Evaluate whether the keywords are used naturally and contextually (not forced or awkward).</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Evaluate Keyword Distribution in the Content</Title>
                    <Details>
                        <Point>Calculate the keyword density (should be within 1–2% of total word count).</Point>
                        <Point>Check for overuse (keyword stuffing) if density > 2.5%.</Point>
                        <Point>Check for the use of LSI (Latent Semantic Indexing) keywords and synonyms to improve semantic richness and avoid repetition (e.g., “AI agent” → “AI assistant”, “autonomous agent”).</Point>
                        <Point>Check if secondary keywords are used properly in H2, H3, or paragraph subheadings.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Identify Issues and Suggest Improvements</Title>
                    <Details>
                        <Point>Point out specific areas if keywords are overused or unnaturally inserted.</Point>
                        <Point>Suggest improvements if keywords are underused or poorly distributed.</Point>
                        <Point>Recommend using keyword variations and natural phrasing to improve readability and SEO quality.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Section title="Overview">
                <Field>Respond in Markdown format.</Field>
                <Field>Overall evaluation of keyword distribution: ...</Field>
                <Field>Score: x/10</Field>
            </Section>

            <Section title="Detailed Evaluation">
                <IssueStructure>
                    <CriterionTitle>Appearance in Title, H1, Meta</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Appearance in First 100 Words</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Keyword Density</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Keyword Stuffing</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Keyword Variations & LSI</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
            </Section>
        </OutputFormat>

        <Content>
            {text}
        </Content>
    </EvaluationRequest>
    """

    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    # print(response.content)
    return response.content

def check_internal_external_links(llm: AzureChatOpenAI, text: str) -> str:  
    """Check internal and external links (internal & backlink).""" 
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>SEO expert</strong> with expertise in analyzing internal and external linking strategies for website content.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>evaluate the link structure</strong> in the article for SEO effectiveness. Focus on the presence, type, placement, and anchor text of both internal and external links.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Analyze Internal Links</Title>
                    <Details>
                        <Point>Check for presence of internal links pointing to:</Point>
                        <Subpoint>- The homepage</Subpoint>
                        <Subpoint>- Category or tag pages (e.g. /ai/, /blockchain/)</Subpoint>
                        <Subpoint>- Related articles (at least 2–3)</Subpoint>
                        <Subpoint>- Itself (canonical/self-reference, if present)</Subpoint>
                        <Point>Verify anchor texts are descriptive and relevant.</Point>
                        <Point>Ensure links are placed naturally within paragraphs or near related content.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Analyze External Links</Title>
                    <Details>
                        <Point>Check if external links use appropriate <code>rel="nofollow"</code> or <code>rel="sponsored"</code> if needed.</Point>
                        <Point>Verify links point to high-authority, relevant sources (not spammy or irrelevant).</Point>
                        <Point>Anchor text should accurately describe the linked content.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Identify Link Issues & Suggest Improvements</Title>
                    <Details>
                        <Point>Flag missing or broken links.</Point>
                        <Point>Flag excessive use of exact match anchor texts (risk of over-optimization).</Point>
                        <Point>Suggest improvements to link diversity, placement, or relevancy.</Point>
                    </Details>
                </Instruction>
            </Mission>

            <OutputFormat>
                <Section title="Overview">
                    <Field>Respond in Markdown format.</Field>
                    <Field>Overall link optimization rating: ...</Field>
                    <Field>Score: x/10</Field>
                </Section>

                <Section title="Detailed Evaluation">
                    <IssueStructure>
                        <CriterionTitle>Internal Link Coverage</CriterionTitle>
                        <Analysis>...</Analysis>
                        <FixSuggestion>...</FixSuggestion>
                    </IssueStructure>
                    <IssueStructure>
                        <CriterionTitle>External Link Quality & Nofollow Usage</CriterionTitle>
                        <Analysis>...</Analysis>
                        <FixSuggestion>...</FixSuggestion>
                    </IssueStructure>
                    <IssueStructure>
                        <CriterionTitle>Anchor Text Relevance</CriterionTitle>
                        <Analysis>...</Analysis>
                        <FixSuggestion>...</FixSuggestion>
                    </IssueStructure>
                    <IssueStructure>
                        <CriterionTitle>Link Placement</CriterionTitle>
                        <Analysis>...</Analysis>
                        <FixSuggestion>...</FixSuggestion>
                    </IssueStructure>
                    <IssueStructure>
                        <CriterionTitle>Technical or Structural Issues</CriterionTitle>
                        <Analysis>...</Analysis>
                        <FixSuggestion>...</FixSuggestion>
                    </IssueStructure>
                </Section>
            </OutputFormat>

            <Content>
                {text}
            </Content>
    </EvaluationRequest>
    """
    response = llm.invoke(prompt)
    # print(response.content)
    return response.content

def check_seo(llm: AzureChatOpenAI, text: str) -> str:
    prompt = f"""
    <seoEvaluationRequest>
        <role>SEO_Expert</role>
        <instructions>
            Hãy đánh giá đoạn nội dung sau theo 6 tiêu chí SEO on-page cơ bản. 
            Trả kết quả từng tiêu chí dưới dạng ✅ (đạt), ⚠️ (cần cải thiện), hoặc ❌ (chưa đạt).
            Nếu có thể, hãy kèm theo gợi ý cải thiện ngắn gọn.
        </instructions>
        <criteria>
            <criterion>
                <name>Upload Title & Meta SEO cho social</name>
                <description>Kiểm tra có title/meta tag và các thẻ Open Graph (og:title, og:description, og:image) chưa.</description>
            </criterion>
            <criterion>
                <name>Thêm H1</name>
                <description>Kiểm tra bài viết có đúng 1 thẻ tiêu đề H1 không.</description>
            </criterion>
            <criterion>
                <name>Định dạng H2, H3</name>
                <description>Kiểm tra việc chia nội dung bằng các heading phụ H2, H3 có hợp lý không.</description>
            </criterion>
            <criterion>
                <name>Check title SEO</name>
                <description>Kiểm tra tiêu đề chính có dưới 60 ký tự và chứa từ khóa chính hay không.</description>
            </criterion>
            <criterion>
                <name>Check meta description SEO</name>
                <description>Kiểm tra bài viết có phần mô tả meta dài khoảng 140–160 ký tự và có sức hấp dẫn hay không.</description>
            </criterion>
            <criterion>
                <name>Tối ưu URL</name>
                <description>Đánh giá URL có ngắn gọn, chứa từ khóa chính và tránh từ dư thừa (stop word) không.</description>
            </criterion>
        </criteria>
        <content format="markdown">
            <![CDATA[
                {text}
            ]]>
        </content>
    </seoEvaluationRequest>
    """

    response = llm.invoke(prompt)
    # print(response.content)
    return response.content

if __name__ == "__main__":
    from langchain_openai import AzureChatOpenAI
    from dotenv import load_dotenv
    import os

    load_dotenv()
    
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

    llm = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model="o3-mini",
        api_version="2024-12-01-preview",
        # temperature=0.7,
        # max_tokens=16000
    )

    # check_keyword_distribution(llm,content)

    # check_internal_external_links(llm,content)

    check_seo(llm,content)