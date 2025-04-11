from langchain_openai import AzureChatOpenAI
from check_seo_module import check_seo,check_internal_external_links,check_keyword_distribution

def check_article_structure(llm: AzureChatOpenAI, text: str) -> str:  
    """Check the structure of the article based on predefined rules."""  

    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>web content evaluation expert</strong> with professional experience in optimizing article structures.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>check and evaluate the structure of the article</strong> based on technical and academic criteria.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Check the main components</Title>
                    <Details>
                        <Point>Title: Is it appropriately long and does it accurately reflect the content of the article?</Point>
                        <Point>Summary (Key Insights): Does it briefly describe the problem, insights, and results of the article?</Point>
                        <Point>Introduction & Objective: Does it clearly state the research problem and objectives?</Point>
                        <Point>Detailed Presentation: Does it delve into the aspects of the problem?</Point>
                        <Point>Conclusion: Does it explain, discuss, and highlight the significance of the results?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Analyze detailed aspects</Title>
                    <Details>
                        <Point>Technology/Model Analysis: Is it clearly presented?</Point>
                        <Point>Position and Competitors: Is it comprehensively evaluated?</Point>
                        <Point>Applications: Are real-world applications clearly stated?</Point>
                        <Point>Financial/Parameter/Valuation Analysis: Are supporting data provided?</Point>
                        <Point>Investment Perspective: Are reasonable viewpoints presented?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Identify issues and suggest improvements</Title>
                    <Details>
                        <Point>If any component is missing, list specific errors.</Point>
                        <Point>If the structure is illogical, suggest a reorganization.</Point>
                        <Point>Provide suggestions to optimize each section for higher quality.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Field>Respond in Markdown format.</Field>
            <Field>Respond in English. Only quoted content should remain in Vietnamese.</Field>
            <Section title="Overview">
                <Field>Overall evaluation of the structure: ...</Field>
                <Field>Score: x/10</Field>
            </Section>

            <Section title="Detailed Evaluation">
                <IssueStructure>
                    <CriterionTitle>Title</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Summary (Key Insights)</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Introduction & Objective</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Detailed Presentation</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Conclusion</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
            </Section>>
        </OutputFormat>

        <Content>
            {text}
        </Content>
    </EvaluationRequest>
    """
    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    # with open("output/check_article_struture.txt", "w", encoding="utf-8") as f:
    #     f.write(response.content)
    return response.content

def check_content(llm: AzureChatOpenAI, text: str) -> str:
    """Evaluate the content of each section of the article based on predefined rules."""
    
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>content evaluation expert</strong> with in-depth analysis experience and expertise in assessing article quality.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>evaluate the content of each section of the article in GREAT DETAIL</strong> based on predefined criteria, ensuring the article achieves the highest quality.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Key Insights</Title>
                    <Details>
                        <Point>Summarize the main points of the article briefly.</Point>
                        <Point>Identify the main issue the article will analyze.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Overview of the Research Topic</Title>
                    <Details>
                        <Point>Introduce the topic or project, including its development history and current status.</Point>
                        <Point>Highlight the problem or challenge to be addressed.</Point>
                        <Point>Clearly define the objectives of the article.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Detailed Analysis</Title>
                    <Details>
                        <Point>Use market data and case studies to support arguments. Ensure the analysis is backed by specific examples and real-world applications.</Point>
                        <Point>Only use data from reputable sources, ensuring high accuracy and reliability. Data must be filtered, analyzed, and processed objectively.</Point>
                        <Point>Avoid imposing subjective opinions; respect the objectivity of events and data.</Point>
                    </Details>
                    <SubInstruction>
                        <Title>3.1 Technology Analysis</Title>
                        <Details>
                            <Point>Explain the foundational technology: Analyze the core technology of the project, reasons for its development, and technical highlights.</Point>
                            <Point>Compare with other technologies: Highlight strengths and weaknesses compared to similar solutions in the market.</Point>
                            <Point>Analyze performance and scalability: Evaluate processing capabilities, performance, scalability potential, and potential issues.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.2 Position and Competitors</Title>
                        <Details>
                            <Point>Compare with competitors: Analyze the project's position in the market, using data to substantiate.</Point>
                            <Point>Evaluate market potential and growth opportunities: Analyze the project's future opportunities and challenges.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.3 Applications</Title>
                        <Details>
                            <Point>Provide specific use cases: Examples of how the project or technology is applied in practice (DeFi, NFT, blockchain infrastructure, etc.).</Point>
                            <Point>Analyze impact on users and the market: Draw lessons or predictions for the future.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.4 Financial/Parameter/Valuation Analysis</Title>
                        <Details>
                            <Point>Financial analysis: Evaluate financial indicators such as trading volume, locked value (TVL), and financial performance.</Point>
                            <Point>Valuation and growth potential: Provide valuation scenarios based on market and intrinsic factors.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.5 Investment Perspective</Title>
                        <Details>
                            <Point>Provide strategies and investment methods: Evaluate the feasibility and effectiveness of each method.</Point>
                            <Point>Analyze risks and opportunities: Suggest measures to mitigate risks.</Point>
                        </Details>
                    </SubInstruction>
                </Instruction>

                <Instruction>
                    <Title>4. Conclusion</Title>
                    <Details>
                        <Point>Summarize the main points discussed.</Point>
                        <Point>Highlight new narratives or development potential of the project.</Point>
                        <Point>Provide a call to action or suggestions for readers.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Field>Respond in Markdown format.</Field>
            <Field>Respond in English. Only quoted content should remain in Vietnamese.</Field>
            <Section title="Overview">
                <Field>Overall evaluation of the content: ...</Field>
                <Field>Score: x/10</Field>
            </Section>

            <Section title="Detailed Evaluation">
                <IssueStructure>
                    <CriterionTitle>Key Insights</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Overview of the Topic</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Detailed Analysis</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Conclusion</CriterionTitle>
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
    # with open("output/check_content.txt", "w", encoding="utf-8") as f:
    #     f.write(response.content)
    return response.content

def check_grammar_error(llm: AzureChatOpenAI, text: str) -> str:
    """Check grammar, spelling, style, and content requirements related to web3, blockchain, crypto, and smart-contract."""
    
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>language expert</strong> with in-depth evaluation experience in the field of <strong>web3, blockchain, crypto, and smart-contract</strong>.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>check and evaluate the style, grammar, and spelling</strong> of the article, ensuring the content meets the highest standards of quality and relevance to the specialized field.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Check grammar and spelling</Title>
                    <Details>
                        <Point>Identify grammatical, spelling, and punctuation errors.</Point>
                        <Point>Ensure sentences are clear, grammatically correct, and unambiguous.</Point>
                        <Point>Quote the erroneous sentences in Vietnamese and suggest corrections in English.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Check style and length</Title>
                    <Details>
                        <Point>Ensure professional style suitable for the field of web3, blockchain, crypto, and smart-contract.</Point>
                        <Point>Check the article length, ensuring a minimum of 2500 words.</Point>
                        <Point>Identify overly long or short paragraphs and suggest ways to split or expand content.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Check for word repetition</Title>
                    <Details>
                        <Point>Identify unnecessary word repetition (except for important keywords).</Point>
                        <Point>Suggest synonyms or alternative expressions to avoid repetition.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>4. Evaluate coherence and linkage</Title>
                    <Details>
                        <Point>Ensure paragraphs have logical connections, not disjointed.</Point>
                        <Point>Check if the main ideas are clearly and coherently presented.</Point>
                        <Point>Suggest improvements if needed.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>5. Suggest improvements</Title>
                    <Details>
                        <Point>If the article can be improved in style, grammar, or presentation, provide specific suggestions.</Point>
                        <Point>Ensure the article is easy to read and understand while maintaining high professionalism.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Field>Respond in Markdown format.</Field>
            <Field>Respond in English. Only quoted content should remain in Vietnamese.</Field>
            <Section title="Overview">
                <Field>Overall evaluation of grammar, spelling, and style: ...</Field>
                <Field>Score: x/10</Field>
            </Section>

            <Section title="Detailed Evaluation">
                <IssueStructure>
                    <CriterionTitle>Grammar and Spelling</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Style and Length</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Word Repetition</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Coherence and Linkage</CriterionTitle>
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
    # with open("output/check_grammar_error.txt", "w", encoding="utf-8") as f:
    #     f.write(response.content)
    return response.content

def evaluate_readability(llm: AzureChatOpenAI, text: str) -> str:  
    """Evaluate the readability and style of the article."""  
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>language and content optimization expert</strong> with experience in evaluating readability and style of articles.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>evaluate the readability and style of the article</strong>, ensuring the content is clear, coherent, easy to understand, yet professional and suitable for the target audience.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Evaluate readability</Title>
                    <Details>
                        <Point>Calculate readability score based on Flesch-Kincaid or equivalent index.</Point>
                        <Point>Are sentences too long or complex?</Point>
                        <Point>Is the language simple and easy to understand or overly academic?</Point>
                        <Point>Is paragraph length reasonable? (Too long can be hard to read)</Point>
                        <Point>Are lists and bullet points used to enhance content absorption?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Evaluate style</Title>
                    <Details>
                        <Point>Is the style suitable for the target audience? (Highly technical, general, marketing...)</Point>
                        <Point>Is the language accurate, objective, avoiding emotional bias?</Point>
                        <Point>Are sentences clear, not ambiguous or misleading?</Point>
                        <Point>Is the tone consistent? (Avoid mixing formal and casual)</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Suggest improvements</Title>
                    <Details>
                        <Point>If sentences are too long or complex, suggest rewriting them more concisely.</Point>
                        <Point>If paragraphs are too dense, suggest splitting them into reasonable sections.</Point>
                        <Point>If the article lacks lists or specific examples, suggest ways to add them.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Section title="Overview">
                <Field>Respond in Markdown format.</Field>
                <Field>Overall readability evaluation: ...</Field>
                <Field>Readability score (based on Flesch-Kincaid or equivalent): x/100</Field>
                <Field>General comments on style: ...</Field>
            </Section>

            <Section title="Detailed Evaluation">
                <IssueStructure>
                    <CriterionTitle>Sentence Length</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Paragraph Length</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Language & Understandability</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Style & Tone</CriterionTitle>
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
    return response.content

def check_uniqueness(llm: AzureChatOpenAI, text: str) -> str:  
    """Check the uniqueness of the content."""  
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>plagiarism detection and uniqueness evaluation expert</strong> for article content.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>check the level of content duplication</strong>, ensuring the article is unique, not copied or overly borrowed from other sources without creativity or added value.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Check for content duplication</Title>
                    <Details>
                        <Point>Identify sections that may have been copied from other sources.</Point>
                        <Point>Compare with popular texts, public documents, and web articles.</Point>
                        <Point>If duplication is found, quote the original text and determine the level of duplication.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Evaluate uniqueness</Title>
                    <Details>
                        <Point>Does the article provide unique perspectives, analyses, or expressions?</Point>
                        <Point>Is it creative or merely repeating information from other sources?</Point>
                        <Point>If the article cites materials, are sources clearly stated?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Suggest edits if necessary</Title>
                    <Details>
                        <Point>If a section can be rewritten to be more distinctive, suggest alternative phrasing.</Point>
                        <Point>If citation sources need to be added, point out specific locations.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Section title="Overview">
                <Field>Respond in Markdown format.</Field>
                <Field>Uniqueness level: x%</Field>
                <Field>General comments: ...</Field>
            </Section>

            <Section title="Detailed Duplication Findings">
                <IssueStructure>
                    <OriginalText>"..."</OriginalText>
                    <Source>Found duplicate with: [URL/Source]</Source>
                    <SimilarityLevel>x%</SimilarityLevel>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <!-- Repeat if multiple duplicate sections -->
            </Section>

            <Section title="Improvement Suggestions">
                <FixStructure>
                    <OriginalText>"..."</OriginalText>
                    <SuggestedRewrite>...</SuggestedRewrite>
                    <Reason>...</Reason>
                </FixStructure>
                <!-- Repeat if necessary -->
            </Section>
        </OutputFormat>

        <Content>
            {text}
        </Content>
    </EvaluationRequest>
    """

    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    return response.content

def evaluate_research_depth(llm: AzureChatOpenAI, text: str) -> str:  
    """Evaluate the depth of research and level of evidence."""  
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>content evaluation expert</strong> with high standards, requiring articles to have <strong>deep research</strong> and <strong>convincing evidence</strong>.
        </Role>

        <Mission>
            <Overview>
                You need to <strong>evaluate the depth of research</strong> of the article below, considering the use of references, data, and evidence supporting arguments.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Determine the level of research</Title>
                    <Details>
                        <Point>Does the article <strong>use reliable references?</strong> (credible sources such as scientific studies, reports, books, official articles).</Point>
                        <Point>If no references are provided, <strong>point out weaknesses</strong> and suggest suitable sources.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Evaluate the level of evidence</Title>
                    <Details>
                        <Point>Does the article **use specific data and statistics** to support arguments?</Point>
                        <Point>If data is provided, **check if the source is credible** (avoid Wikipedia, personal blogs, unclear sources).</Point>
                        <Point>If the article only provides **general arguments without evidence**, point out weaknesses and suggest improvements.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Evaluate comparisons and multi-dimensional perspectives</Title>
                    <Details>
                        <Point>Does the article consider **different perspectives** on the issue?</Point>
                        <Point>If the article only provides one-sided views, suggest adding other perspectives to increase objectivity.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>4. Check the level of in-depth analysis</Title>
                    <Details>
                        <Point>Does the article delve into the issue, providing detailed analysis?</Point>
                        <Point>If it only scratches the surface, suggest ways to delve deeper into key points.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <Criteria>
            <Criterion>
                <Title>1. Research & References (10 points)</Title>
                <Checklist>
                    <Item>Are reliable references used?</Item>
                    <Item>Avoid Wikipedia, personal blogs?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>2. Level of Evidence (10 points)</Title>
                <Checklist>
                    <Item>Are data and statistics used?</Item>
                    <Item>Are data sources credible?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>3. Comparisons and Multi-Dimensional Perspectives (10 points)</Title>
                <Checklist>
                    <Item>Are different perspectives considered?</Item>
                    <Item>Are differences between perspectives analyzed?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>4. Depth of Analysis (10 points)</Title>
                <Checklist>
                    <Item>Does the article delve into the issue?</Item>
                    <Item>Or does it only scratch the surface?</Item>
                </Checklist>
            </Criterion>
        </Criteria>

        <OutputFormat>
            <Section title="Overview">
                <Field>Respond in Markdown format.</Field>
                <Field>Total score: .../40</Field>
                <Field>General comments: ...</Field>
            </Section>

            <Section title="Detailed Evaluation of Each Criterion">
                <CriterionEvaluation>
                    <CriterionTitle>1. Research & References: x/10</CriterionTitle>
                    <Pros>✅ Strengths: ...</Pros>
                    <Cons>❌ Weaknesses: ...</Cons>
                    <Suggestions>💡 Suggestions: ...</Suggestions>
                </CriterionEvaluation>

                <CriterionEvaluation>
                    <CriterionTitle>2. Level of Evidence: x/10</CriterionTitle>
                    <Pros>✅ Strengths: ...</Pros>
                    <Cons>❌ Weaknesses: ...</Cons>
                    <Suggestions>💡 Suggestions: ...</Suggestions>
                </CriterionEvaluation>

                <CriterionEvaluation>
                    <CriterionTitle>3. Comparisons and Multi-Dimensional Perspectives: x/10</CriterionTitle>
                    <Pros>✅ Strengths: ...</Pros>
                    <Cons>❌ Weaknesses: ...</Cons>
                    <Suggestions>💡 Suggestions: ...</Suggestions>
                </CriterionEvaluation>

                <CriterionEvaluation>
                    <CriterionTitle>4. Depth of Analysis: x/10</CriterionTitle>
                    <Pros>✅ Strengths: ...</Pros>
                    <Cons>❌ Weaknesses: ...</Cons>
                    <Suggestions>💡 Suggestions: ...</Suggestions>
                </CriterionEvaluation>
            </Section>
        </OutputFormat>

        <Content>
            --- START OF ARTICLE TO BE EVALUATED ---
            {text}
            --- END OF ARTICLE ---
        </Content>
    </EvaluationRequest>
    """
    
    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    return response.content

def check_text(llm: AzureChatOpenAI, text: str) -> str:
    """Comprehensive content evaluation of the article"""

    check_keyword_distribution_result = check_keyword_distribution(llm,text)
    check_internal_external_links_result = check_internal_external_links(llm,text)
    check_seo_result = check_seo(llm,text)
    check_article_structure_result = check_article_structure(llm,text)
    check_content_result = check_content(llm,text)
    check_grammar_error_result = check_grammar_error(llm,text)

    sumarize_result = f"""
#Results of keyword distribution evaluation:
{check_keyword_distribution_result}

#Results of internal and external links evaluation:
{check_internal_external_links_result}

#Results of SEO evaluation:
{check_seo_result}

#Results of structure evaluation based on article requirements:
{check_article_structure_result}

#Results of content evaluation based on article requirements:
{check_content_result}

#Results of grammar, spelling, style, and length evaluation:
{check_grammar_error_result}
    """

    sumarize_result.replace("```","")

    final_result = llm.invoke(f"""
    Please format the following content into a well-structured and visually appealing Markdown format. Use headings, subheadings, bullet points, and other Markdown elements to enhance readability and organization. Ensure the content is easy to navigate and visually clean. Only return the formatted result without any explanations or additional comments.
    Content to format:
    {sumarize_result}
    """).content
    
    # with open("output/check_text.txt", "w", encoding="utf-8") as f:
    #     f.write(final_result)
    # print(final_result)
    return final_result

if __name__ == "__main__":
    import os
    import extract_module
    from langchain_openai import AzureChatOpenAI
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()

    # Initialize Azure OpenAI API with credentials and configuration
    llm = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model="o3-mini",
        api_version="2024-12-01-preview",
        # temperature=0.7,
        # max_tokens=16000
    )

    text = """
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

    # check_article_structure(llm, text)

    # check_content(llm,text)

    # check_grammar_error(llm,text)

    check_text(llm,text)