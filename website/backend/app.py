import os
import json
import uvicorn
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
















# For storing static variables



US_AREA_CODES = {
    "201": "New Jersey",
    "202": "Washington DC",
    "203": "Connecticut",
    "205": "Alabama",
    "206": "Washington",
    "207": "Maine",
    "208": "Idaho",
    "209": "California",
    "210": "Texas",
    "212": "New York",
    "213": "California",
    "214": "Texas",
    "215": "Pennsylvania",
    "216": "Ohio",
    "217": "Illinois",
    "218": "Minnesota",
    "219": "Indiana",
    "220": "Ohio",
    "223": "Pennsylvania",
    "224": "Illinois",
    "225": "Louisiana",
    "227": "Maryland",
    "228": "Mississippi",
    "229": "Georgia",
    "231": "Michigan",
    "234": "Ohio",
    "235": "Missouri",
    "239": "Florida",
    "240": "Maryland",
    "248": "Michigan",
    "251": "Alabama",
    "252": "North Carolina",
    "253": "Washington",
    "254": "Texas",
    "256": "Alabama",
    "260": "Indiana",
    "262": "Wisconsin",
    "267": "Pennsylvania",
    "269": "Michigan",
    "270": "Kentucky",
    "272": "Pennsylvania",
    "274": "Wisconsin",
    "276": "Virginia",
    "279": "California",
    "281": "Texas",
    "283": "Ohio",
    "301": "Maryland",
    "302": "Delaware",
    "303": "Colorado",
    "304": "West Virginia",
    "305": "Florida",
    "307": "Wyoming",
    "308": "Nebraska",
    "309": "Illinois",
    "310": "California",
    "312": "Illinois",
    "313": "Michigan",
    "314": "Missouri",
    "315": "New York",
    "316": "Kansas",
    "317": "Indiana",
    "318": "Louisiana",
    "319": "Iowa",
    "320": "Minnesota",
    "321": "Florida",
    "323": "California",
    "324": "Florida",
    "325": "Texas",
    "326": "Ohio",
    "327": "Arkansas",
    "329": "New York",
    "330": "Ohio",
    "331": "Illinois",
    "332": "New York",
    "334": "Alabama",
    "336": "North Carolina",
    "337": "Louisiana",
    "339": "Massachusetts",
    "341": "California",
    "346": "Texas",
    "347": "New York",
    "350": "California",
    "351": "Massachusetts",
    "352": "Florida",
    "353": "Wisconsin",
    "360": "Washington",
    "361": "Texas",
    "363": "New York",
    "364": "Kentucky",
    "369": "California",
    "380": "Ohio",
    "385": "Utah",
    "386": "Florida",
    "401": "Rhode Island",
    "402": "Nebraska",
    "404": "Georgia",
    "405": "Oklahoma",
    "406": "Montana",
    "407": "Florida",
    "408": "California",
    "409": "Texas",
    "410": "Maryland",
    "412": "Pennsylvania",
    "413": "Massachusetts",
    "414": "Wisconsin",
    "415": "California",
    "417": "Missouri",
    "419": "Ohio",
    "423": "Tennessee",
    "424": "California",
    "425": "Washington",
    "430": "Texas",
    "432": "Texas",
    "434": "Virginia",
    "435": "Utah",
    "436": "Ohio",
    "440": "Ohio",
    "442": "California",
    "443": "Maryland",
    "445": "Pennsylvania",
    "447": "Illinois",
    "448": "Florida",
    "458": "Oregon",
    "463": "Indiana",
    "464": "Illinois",
    "469": "Texas",
    "470": "Georgia",
    "472": "North Carolina",
    "475": "Connecticut",
    "478": "Georgia",
    "479": "Arkansas",
    "480": "Arizona",
    "484": "Pennsylvania",
    "501": "Arkansas",
    "502": "Kentucky",
    "503": "Oregon",
    "504": "Louisiana",
    "505": "New Mexico",
    "507": "Minnesota",
    "508": "Massachusetts",
    "509": "Washington",
    "510": "California",
    "512": "Texas",
    "513": "Ohio",
    "515": "Iowa",
    "516": "New York",
    "517": "Michigan",
    "518": "New York",
    "520": "Arizona",
    "530": "California",
    "531": "Nebraska",
    "534": "Wisconsin",
    "539": "Oklahoma",
    "540": "Virginia",
    "541": "Oregon",
    "551": "New Jersey",
    "557": "Missouri",
    "559": "California",
    "561": "Florida",
    "562": "California",
    "563": "Iowa",
    "564": "Washington",
    "567": "Ohio",
    "570": "Pennsylvania",
    "571": "Virginia",
    "572": "Oklahoma",
    "573": "Missouri",
    "574": "Indiana",
    "575": "New Mexico",
    "580": "Oklahoma",
    "582": "Pennsylvania",
    "585": "New York",
    "586": "Michigan",
    "601": "Mississippi",
    "602": "Arizona",
    "603": "New Hampshire",
    "605": "South Dakota",
    "606": "Kentucky",
    "607": "New York",
    "608": "Wisconsin",
    "609": "New Jersey",
    "610": "Pennsylvania",
    "612": "Minnesota",
    "614": "Ohio",
    "615": "Tennessee",
    "616": "Michigan",
    "617": "Massachusetts",
    "618": "Illinois",
    "619": "California",
    "620": "Kansas",
    "623": "Arizona",
    "624": "New York",
    "626": "California",
    "628": "California",
    "629": "Tennessee",
    "630": "Illinois",
    "631": "New York",
    "636": "Missouri",
    "640": "New Jersey",
    "641": "Iowa",
    "645": "Florida",
    "646": "New York",
    "650": "California",
    "651": "Minnesota",
    "656": "Florida",
    "657": "California",
    "659": "Alabama",
    "660": "Missouri",
    "661": "California",
    "662": "Mississippi",
    "667": "Maryland",
    "669": "California",
    "678": "Georgia",
    "680": "New York",
    "681": "West Virginia",
    "682": "Texas",
    "686": "Virginia",
    "689": "Florida",
    "701": "North Dakota",
    "702": "Nevada",
    "703": "Virginia",
    "704": "North Carolina",
    "706": "Georgia",
    "707": "California",
    "708": "Illinois",
    "712": "Iowa",
    "713": "Texas",
    "714": "California",
    "715": "Wisconsin",
    "716": "New York",
    "717": "Pennsylvania",
    "718": "New York",
    "719": "Colorado",
    "720": "Colorado",
    "724": "Pennsylvania",
    "725": "Nevada",
    "726": "Texas",
    "727": "Florida",
    "728": "Florida",
    "730": "Illinois",
    "731": "Tennessee",
    "732": "New Jersey",
    "734": "Michigan",
    "737": "Texas",
    "740": "Ohio",
    "743": "North Carolina",
    "747": "California",
    "754": "Florida",
    "757": "Virginia",
    "760": "California",
    "762": "Georgia",
    "763": "Minnesota",
    "765": "Indiana",
    "769": "Mississippi",
    "770": "Georgia",
    "771": "Washington DC",
    "772": "Florida",
    "773": "Illinois",
    "774": "Massachusetts",
    "775": "Nevada",
    "779": "Illinois",
    "781": "Massachusetts",
    "785": "Kansas",
    "786": "Florida",
    "801": "Utah",
    "802": "Vermont",
    "803": "South Carolina",
    "804": "Virginia",
    "805": "California",
    "806": "Texas",
    "808": "Hawaii",
    "810": "Michigan",
    "812": "Indiana",
    "813": "Florida",
    "814": "Pennsylvania",
    "815": "Illinois",
    "816": "Missouri",
    "817": "Texas",
    "818": "California",
    "820": "California",
    "826": "Virginia",
    "828": "North Carolina",
    "830": "Texas",
    "831": "California",
    "832": "Texas",
    "835": "Pennsylvania",
    "838": "New York",
    "839": "South Carolina",
    "840": "California",
    "843": "South Carolina",
    "845": "New York",
    "847": "Illinois",
    "848": "New Jersey",
    "850": "Florida",
    "854": "South Carolina",
    "856": "New Jersey",
    "857": "Massachusetts",
    "858": "California",
    "859": "Kentucky",
    "860": "Connecticut",
    "861": "Illinois",
    "862": "New Jersey",
    "863": "Florida",
    "864": "South Carolina",
    "865": "Tennessee",
    "870": "Arkansas",
    "872": "Illinois",
    "878": "Pennsylvania",
    "901": "Tennessee",
    "903": "Texas",
    "904": "Florida",
    "906": "Michigan",
    "907": "Alaska",
    "908": "New Jersey",
    "909": "California",
    "910": "North Carolina",
    "912": "Georgia",
    "913": "Kansas",
    "914": "New York",
    "915": "Texas",
    "916": "California",
    "917": "New York",
    "918": "Oklahoma",
    "919": "North Carolina",
    "920": "Wisconsin",
    "925": "California",
    "928": "Arizona",
    "929": "New York",
    "930": "Indiana",
    "931": "Tennessee",
    "934": "New York",
    "936": "Texas",
    "937": "Ohio",
    "938": "Alabama",
    "940": "Texas",
    "941": "Florida",
    "943": "Georgia",
    "945": "Texas",
    "947": "Michigan",
    "948": "Virginia",
    "949": "California",
    "951": "California",
    "952": "Minnesota",
    "954": "Florida",
    "956": "Texas",
    "959": "Connecticut",
    "970": "Colorado",
    "971": "Oregon",
    "972": "Texas",
    "973": "New Jersey",
    "975": "Missouri",
    "978": "Massachusetts",
    "979": "Texas",
    "980": "North Carolina",
    "983": "Colorado",
    "984": "North Carolina",
    "985": "Louisiana",
    "986": "Idaho",
    "989": "Michigan"
}

RESUME_FORMATTING_PROMPT_1 = """
INPUT RESUME:
```
{{{INPUT}}}
```

You are a professional resume formatter. You will receive a candidate's CV (in any language) as an attachment. Your job is to standardize the candidate's resume in the INPUT RESUME, where it will be programmatically converted into a word document and filled out and checked by an employee at a professional executive search firm based in China.

---

RULES:

1. EXTRACT, DON'T INVENT. Only populate fields if the information is explicitly present in the CV. Leave fields blank if the information is not available. Never guess or infer.

2. PROFESSIONAL EXPERIENCE MUST BE WORD FOR WORD. Copy the bullet point content from the original CV exactly as written - do not summarize, rephrase, shorten, or paraphrase any bullet points. The only exception is if the CV is not in English, in which case you must translate it faithfully and completely. Every bullet point, sub-bullet, and line of content must be preserved.

3. ALL SECTIONS MUST ALWAYS BE PRESENT. Even if a section is empty, include it. Do not skip any section or subsection.

4. FORMATTING IS STRICT. Follow the rules below for each section:

   PERSONAL INFORMATION section (everything above "Assessment on Candidate:"):
   - No tabs, no extra spaces, no inconsistent indentation. Use a single space after each colon.

   Below there are multiple Formatting Guidelines for different sections with code chunks below them. Follow anything not inside brackets "[]" EXACTLY, in a literal sense: the number of newline characters, the positions of the spaces, the number of spaces, the string literal "-", capitalization convention, and the use of 4 spaces in a row (not indentation tabs).

   Experience Formatting Guideline 1 (single role at a company):
```
[MM/YY] - [MM/YY or Now] | [Company Name]
    [Position Title]

Responsibilities:
- [bullet point]
- [bullet point]
```

   Experience Formatting Guideline 2 (multiple roles at the same company - use "Responsibilities:" once):
```
[MM/YY] - [MM/YY or Now] | [Company Name]
    [Most Recent Position Title]

Responsibilities:
- [MM/YY] - [MM/YY] | [Role Title]
- [bullet point]
- [bullet point]

- [MM/YY] - [MM/YY] | [Earlier Role Title]
- [bullet point]
```

   Experience Formatting Guideline 3 (role has both a summary paragraph and bullet points):
```
[MM/YY] - [MM/YY or Now] | [Company Name]
    [Most Recent Position Title]

Responsibilities:
- [MM/YY] - [MM/YY] | [Role Title]
[Summary paragraph]
- [bullet point]
- [bullet point]
```

   Experience Section Clarification: The number of bullet points is not required to be 2 - add as many as there actually are in the input resume. Repeat the same format for each company in the input resume.

   Experience Section Clarification: If the candidate wrote a single long paragraph describing a position/role instead of bullet points, break it down into bullet points with minimal changes to the text content.

   Education Formatting Guideline:
```
[MM/YY] - [MM/YY] | [University Name]
    [Degree / Major]
```

5. EDUCATION: Extract only institution name, degree, and dates. Do not include course lists, GPA, honours, scholarships, or exchange experiences.

6. LANGUAGE: If the candidate's CV is in Chinese or another language, produce the output in English.

---

TEMPLATE:
```
Position Recommended:


Personal Information:

Name: [full name]
Gender: [gender]
Date of Birth: [DOB]
Nationality: [nationality]
Marriage Status: [status]
Current Location: [city/country]
Language: English: [level]
Mandarin: [level]


Education Background:

[MM/YY] - [MM/YY] | [University Name]
    [Degree / Major]

[Repeat for each degree, most recent first]


Assessment on Candidate:


Professional Experience:

[MM/YY] - [MM/YY or Now] | [Company Name]
    [Most recent job title at this company]

Responsibilities:
- [bullet point copied word for word from CV]
- [bullet point copied word for word from CV]

[Repeat block for each company, most recent first]


Compensation:

Current Salary:
Salary Expectation:


End of Profile
```

(Note: Starting from the end of the "Personal Information:" section, use 2 newline characters after the end of a section before beginning a new one)

---


EXAMPLE 1 - Formatted Output:

```
Position Recommended:


Personal Information:

Name: Liu Bin Wu
Gender: Male
Date of Birth:
Nationality:
Marriage Status:
Current Location:
Language: English: Fluent
Mandarin: Fluent


Education Background:

2008/09 - 2009/12 | University of Newcastle Upon Tyne, UK
    Master of Arts

2005/09 - 2008/07 | Northumbria University, UK
    Bachelor of Science


Assessment on Candidate:

[leave empty]


Professional Experience:

2022/06 - Now | HSBC
    Global Banking and Markets, Vice President - Institutional Client Group

Responsibilities:
- 2024/07 - 2025/01 | HSBC US Securities Hedge Fund Coverage
- To maintain and develop relationship with Chinese fund manager & QFII client and drive for new business initiative for the sector.
- To execute ICG strategy to grow revenue across allocated portfolio, and successfully defend/service existing business in addition to originating new value;
- To act as the center of excellence to develop, implement and promote business strategy and risk management initiatives for the Sector in the region, and provide strategic input to senior management;
- Collaboration with internal stakeholder like Global markets, Securities service, Private banking and Innovation banking to promote bank SoW
- To be conversant with the global/local economies and able to respond to business opportunity faster than the Bank's competitors.
- To keep abreast of the trend and development of the Asset Management/Alternative Investment Management sector/industries. Be responsible for the tier 1 hedge fund, quant fund, PE etc

2017/09 - 2022/05 | HSBC
    Commercial Banking, Vice President

Responsibilities:
- Top performer and major relationship manager in middle market clients and top listed POE
- Strong performer and core contributor of the team (Top Rating for consecutive 3 years)
- Rich experience in commercial banking products including trade, cash management and global markets product
- Be responsible for business development, relationship maintenance, and credit proposal
- Exposure to HSBC's investment banking products, DCM, M&A and Leveraged & Acquisition financing etc.

2016/07 - 2017/09 | Wells Fargo
    Capital Finance, Business Development Manager

Responsibilities:
- Responsible for promoting and structuring Supply Chain Finance, Trade Finance solutions to MNC clients
- Credit portfolio with over 35 accounts (SME's, MME's, large corps) and $20MM exposure in USD and CNY
- Managed fully integrated channel financing program for major clients, ensuring smooth program operations & sufficient credit capacity
- Project led successful CNY program launch for key client, incl. execution of new Chinese agreements, syndication with onshore PRC banks
- Negotiate English & Chinese client agreements / legal documentation

2013/02 - 2016/06 | GE Capital
    Commercial Distribution Finance, Business Development Manager

Responsibilities:
- GE Capital CDF business acquired by Wells Fargo on 1 July, 2016
- Develop MNC customer relationship and execute strategies to drive growth, retention and profitability of accounts and optimize market penetration.
- Drive wing-to-wing sales process including customer prospecting, lead generation, making sales calls, analyzing data, preparing proposals and credit packages, negotiating price or other terms, and coordinating onboarding and ongoing relationships with customers.
- Accountable for delivering assigned sales volume and margin target
- Collaborate with both Risk and Capital Markets teams to structure obligor facilities consistent with GE risk policy while delivering adequate credit line capacity
- Responsible to prepare planning and forecast of portfolio performance by working closely with finance team and regional risk team.

2010/04 - 2013/01 | PayPal
    Merchant Service, Strategic Partnership Manager

Responsibilities:
- 2011/04 - 2013/01 | Bank & Payment Gateway & Card Association & Logistics & Social Media & Tech Partner
- Develop agreed high potential partners and offers for enriching acquisition channels & platform
- To own end to end program for ensuring expected sales goal (Revenue & Active Account)
- To continuously train and coach frontline with proven efficient sales model for boosting performance
- To closely co-work with Marketing & Product for more resources & high-quality execution

- 2010/04 - 2011/03 | Project Manager (OSS X-board trade project)
- Develop, launch and operate OSS platform, OSS is an integrated solution designed for merchants who is willing to build their domestic or cross border ecommerce business (RMB40MM transaction volume and 2000 sales leads)
- Design and implement a high technological quality, easy to use and cost-effective solution. Provide expertise on ecommerce supply chain integration, as well as emerging and current internet technologies that may be of interest to the integrated solution.
- Coordinate cross-functional teams and partners. Manage platform and vendors, finalize China OSS 2.0 portal and super roll it out with needed adaptations in other APAC markets.

- Project Coordinate (Global Partner Program)
- Review business requirements, scope and project plans, and gather feedback from PayPal CN/APAC team members to further input in this area.
- Work with country teams to implement required services, product and potential partners
- Design CN Partner portal onboarding process, terms and conditions.

2009/09 - 2010/03 | Deutsche Bank
    Country Management, Assistant of Branch Manager (CBRC Inspection project)

Responsibilities:
- Approaching potential customers, and establishing good relationship with existing and walk-in customers.
- Maintaining service enhancement in cultivating the Sales & Service culture, ensuring professional environment of the bank hail and handling difficult situations to meet customer satisfaction
- Assisting management reporting and updating information on the database - Making preparation for business letter and invitation


Compensation:

Current Salary:
Salary Expectation:

End of Profile
```


EXAMPLE 2 - Formatted Output:

```
Position Recommended:

Personal Information:

Name: Aggie (Yujing) GE
Gender:
Date of Birth:
Nationality:
Marriage Status:
Current Location:
Language: English: Fluent
Mandarin: Fluent


Education Background:

2020/08 - 2022/06 | University of Melbourne
    Management Accounting Master

2017/03 - 2020/06 | University of Sydney
    Finance; Business Analysis; Banking (triple majors)


Assessment on Candidate:

[leave empty]


Professional Experience:

2023/10 - Now | China International Capital Corporation Ltd (CICC)
    OTC commodity sales associate, Fixed Income Department

Responsibilities:
- Core business: with cross-border commodity total return swaps (TRS) and commodity options as the core, to help customers achieve hedging or investment arbitrage purposes
- Customer development: actively develop new customers, and jointly pitch customers with other departments, including presenting onboarding requirements, business scope, transaction processes, and investment research advantages to enhance client acquisition efficiency
- Customer maintenance: focus on providing comprehensive service to existing clients and stabilizing trading volume from key accounts. This was achieved by continuously gaining in-depth understanding of their needs and feedback, and maintaining close communication and collaboration with trading desks and middle/back-office teams to ensure efficient resolution of client issues. Achieved an over 300% year-over-year trading volume growth for a hedge fund client through dedicated relationship management
- "Insurance + Futures" Projects: led and successfully implemented multiple "Insurance + Futures" projects. Utilized customized financial instruments, such as Asian-style enhanced options, to precisely safeguard farmer incomes, thereby strongly supporting the implementation of the rural revitalization strategy.
- Investment and research services: proactively provided clients with theme research conference and customized roadshows services. Also served as a conference moderator, responsible for overall coordination and management.

2022/06 - 2023/10 | Industrial Securities Co.,Ltd
    Investment banking associate, Investment Banking Department

Responsibilities:
- Legal aspects: responsible for preparing the legal part of a Pre-IPO company of the Beijing Stock Exchange and writing the prospectus, including but not limited to the company's history, equity structure, special investment terms, Intra-industry competition, related transactions, major violations of laws and regulations, etc
- Business aspects: responsible for verifying the business part of a Pre-IPO company of the Beijing Stock Exchange during the project initiation period and writing the project initiation report and the business related contents of the project initiation reply, including but not limited to the basic situation of the industry and the company's competition status, the company's main business and products, interviews with customers and suppliers (have done many overseas English interviews), major intangible assets and fixed assets, labor dispatch, social welfare payment, etc
- Other aspects: participated in 4 due diligence investigations; completed 4 project proposals and 2 business plans; written a number of legal memorandums (covered topics including gambling agreements, foreign exchange registration, historical shareholders non-cooperate with interviews, personal income tax involved in share reform, etc.); assisted IPO clients to analyze the positioning and selection of pre-listing sectors and formulated a listing schedule for them

2021/08 - 2022/05 | Huatai United Securities Co., Ltd
    IPO project [688726.SH] undertaking intern, Investment Banking Department

Responsibilities:
- Case research: searched for photovoltaic industry-related research reports and comparable company prospectuses; collected comparable company inquiries about Research and Development costs; assisted in writting memos for intermediary commission
- Financial due diligence: investigated the large amount and abnormal bank cash flow of the issuer, controlling shareholders, directors, supervisors and senior executives, and communicated to obtain supporting materials
- Legal due diligence: assisted in filling basic information for institutional shareholders and key natural persons' questionnaires
- Pitchbook writing: assisted in the designing new energy vehicle project proposals, using segment valuation methods to estimate Tesla's hardware and software business market value respectively

2021/01 - 2021/03 | Deloitte Monitor
    New material group intern, Risk Advisory Department

Responsibilities:
- Underdrawing preparation: provided process risk control services for a large car company, assisted the project team to sort out the company's existing credit rating policies and business processes, reviewed nearly 5000 documents, and produced more than 20 working papers
- Credit rating establishment: assisted the project team to build a credit rating system from four dimensions: financial evaluation, tax evaluation, credit history and risk control capabilities. Each dimension is assigned different evaluation factors and weights to improve the original credit rating scheme and to conduct comprehensive credit ratings for car dealers


Compensation:

Current Salary:
Salary Expectation:

End of Profile
```
""".strip()


RESUME_FORMATTING_PROMPT_1_ZH = """
INPUT RESUME:
```
{{{INPUT}}}
```

You are a professional resume formatter. You will receive a candidate's CV in Chinese as an attachment. Your job is to standardize the candidate's resume in the INPUT RESUME, where it will be programmatically converted into a word document and filled out and checked by an employee at a professional executive search firm based in China.

---

RULES:

1. EXTRACT, DON'T INVENT. Only populate fields if the information is explicitly present in the CV. Leave fields blank if the information is not available. Never guess or infer.

2. PROFESSIONAL EXPERIENCE MUST BE WORD FOR WORD. Copy the bullet point content from the original CV exactly as written in Chinese - do not summarize, rephrase, shorten, or paraphrase any bullet points. Every bullet point, sub-bullet, and line of content must be preserved.

3. ALL SECTIONS MUST ALWAYS BE PRESENT. Even if a section is empty, include it. Do not skip any section or subsection.

4. FORMATTING IS STRICT. Follow the rules below for each section:

   PERSONAL INFORMATION section (everything above "Assessment on Candidate:"):
   - No tabs, no extra spaces, no inconsistent indentation. Use a single space after each colon.

   Below there are multiple Formatting Guidelines for different sections with code chunks below them. Follow anything not inside brackets "[]" EXACTLY, in a literal sense: the number of newline characters, the positions of the spaces, the number of spaces, the string literal "-", capitalization convention, and the use of 4 spaces in a row (not indentation tabs).

   Experience Formatting Guideline 1 (single role at a company):
```
[MM/YY] - [MM/YY or Now] | [Company Name]
    [Position Title]

Responsibilities:
- [bullet point]
- [bullet point]
```

   Experience Formatting Guideline 2 (multiple roles at the same company - use "Responsibilities:" once):
```
[MM/YY] - [MM/YY or Now] | [Company Name]
    [Most Recent Position Title]

Responsibilities:
- [MM/YY] - [MM/YY] | [Role Title]
- [bullet point]
- [bullet point]

- [MM/YY] - [MM/YY] | [Earlier Role Title]
- [bullet point]
```

   Experience Formatting Guideline 3 (role has both a summary paragraph and bullet points):
```
[MM/YY] - [MM/YY or Now] | [Company Name]
    [Most Recent Position Title]

Responsibilities:
- [MM/YY] - [MM/YY] | [Role Title]
[Summary paragraph]
- [bullet point]
- [bullet point]
```

   Experience Section Clarification: The number of bullet points is not required to be 2 - add as many as there actually are in the input resume. Repeat the same format for each company in the input resume.

   Experience Section Clarification: If the candidate wrote a single long paragraph describing a position/role instead of bullet points, break it down into bullet points with minimal changes to the text content.

   Education Formatting Guideline:
```
[MM/YY] - [MM/YY] | [University Name]
    [Degree / Major]
```

5. EDUCATION: Extract only institution name, degree, and dates. Do not include course lists, GPA, honours, scholarships, or exchange experiences.

6. LANGUAGE: The CV is in Chinese. Produce the output in Chinese. Keep all section header labels (Position Recommended:, Personal Information:, Assessment on Candidate:, Education Background:, Professional Experience:, Compensation:, End of Profile) and field labels (Name:, Gender:, Date of Birth:, Nationality:, Marriage Status:, Current Location:, Language:, Mandarin:, English:, Current Salary:, Salary Expectation:) exactly as shown in the template in English. Only the free-text content (bullet points, job titles, company names, degree names, university names) should remain in Chinese.

---

TEMPLATE:
```
Position Recommended:


Personal Information:

Name: [full name]
Gender: [gender]
Date of Birth: [DOB]
Nationality: [nationality]
Marriage Status: [status]
Current Location: [city/country]
Language: English: [level]
Mandarin: [level]


Education Background:

[MM/YY] - [MM/YY] | [University Name]
    [Degree / Major]

[Repeat for each degree, most recent first]


Assessment on Candidate:


Professional Experience:

[MM/YY] - [MM/YY or Now] | [Company Name]
    [Most recent job title at this company]

Responsibilities:
- [bullet point copied word for word from CV]
- [bullet point copied word for word from CV]

[Repeat block for each company, most recent first]


Compensation:

Current Salary:
Salary Expectation:


End of Profile
```

(Note: Starting from the end of the "Personal Information:" section, use 2 newline characters after the end of a section before beginning a new one)
""".strip()






NEW_RESUME_FORMATTING_PROMPT_1_ZH = """
Parsed Candidate Resume:
```
{{{INPUT}}}
```

This is for a professional Executive Search Firm. You are a resume formatter. Your job is to take raw resume text parsed from a PDF and reformat it into a fixed template. You will output ONLY the formatted resume text. Nothing else. No explanations. No comments. No preamble.

HERE IS THE EXACT OUTPUT TEMPLATE YOU MUST FOLLOW:

推荐职位：[BOLD][UNDERLINE]
 
个人详细资料：[BOLD]
 
姓名:    [NAME]
性别:    [GENDER]
出生日期:    [DOB]
国籍:    [NATIONALITY]
婚姻状况:    
目前所在地:    [CITY]
语言能力:    [LANGUAGES]
 
教育背景：[BOLD]
          [START YEAR/MONTH] – [END YEAR/MONTH][BOLD]
          [SCHOOL NAME][BOLD]
          [MAJOR] | [DEGREE][BOLD]
 
证书：[BOLD]
          [CERT 1][BOLD]
          [CERT 2][BOLD]
          [CERT 3][BOLD]
          [CERT 4][BOLD]
          [CERT 5][BOLD]
 
候选人评估：[BOLD]
 
 
工作经验:[BOLD]
 
[START DATE]—[END DATE]         [COMPANY NAME][BOLD]
                                [JOB TITLE][BOLD]
工作职责：
- [DUTY 1]
- [DUTY 2]
- [DUTY 3]
- [DUTY 4]
 
[REPEAT FOR EACH ROLE]
 
 
薪酬福利：[BOLD]
 
目前薪水:[BOLD]
 
期望薪水:[BOLD]
 
离职期:[BOLD]
 
 
End of Profile[BOLD]

---

STRICT RULES. VIOLATING ANY OF THESE IS A FAILURE:

1. OUTPUT ONLY THE FORMATTED RESUME. DO NOT SAY ANYTHING ELSE BEFORE OR AFTER.

2. WORD FOR WORD. DO NOT CHANGE ANY OF THE EXPERIENCE ITEMS. Copy every duty bullet exactly as it appears in the input. Do not rewrite, summarize, shorten, expand, or rephrase anything.

3. DO NOT CHANGE THE NUMBER OF SPACES. THE LARGE GROUPS OF SPACES AND SPACING AFTER SEMICOLONS (```:    ```) IS DELIBERATE. Copy them exactly.

4. DO NOT REMOVE ANY OF THE SECTIONS IF THEY ARE EMPTY. EVERYTHING IS ON THERE FOR A REASON. THIS IS NOT SOMETHING YOU ARE THE DECISION MAKER FOR. If 婚姻状况, 目前薪水, 期望薪水, 离职期, or 候选人评估 are empty, leave them empty. Keep the line. Keep the spacing.

5. DATE FORMAT: Convert dates like "2024年08月" to "2024/08" and ranges like "2024年08月 - 2025年07月" to "2024/08—2025/07". No spaces around the dash.

6. CERTIFICATES go under 证书：. Languages go on the 语言能力 line in 个人详细资料. DO NOT put languages under 证书：.

7. COMPANY LINE FORMAT: [DATE RANGE]         [COMPANY NAME][BOLD] — exactly 9 spaces between date and company name.
   TITLE LINE FORMAT:                       [JOB TITLE][BOLD] — exactly 22 spaces of indentation.

8. EDUCATION indentation: exactly 10 spaces before each line inside 教育背景.

9. CERTIFICATES indentation: exactly 10 spaces before each line inside 证书.

10. Every duty bullet must start with - followed by a space.

11. [BOLD] and [UNDERLINE] tags must appear exactly as shown in the template. Do not add them to any line not shown in the template. Do not remove them from any line shown in the template.

12. IGNORE any watermark lines like "新坦达(上海)资产管理有限公司 招聘专用". Do not include them in the output.

13. 工作职责： lines are NOT bold. Do not add [BOLD] to them.

14. Duty bullets are NOT bold. Do not add [BOLD] to them.

15. The 个人详细资料 field lines (姓名, 性别, etc.) are NOT bold. Do not add [BOLD] to them.
""".strip()










RESUME_FORMATTING_PROMPT_2 = """
This is the candidates resume:
```
{{{INPUT}}}
```

Your task is to process a formatted resume. Your goal is to format the resume so that it looks like a presentable PDF document by writing and inserting html code into it to make parts of it bold, control the font sizes, and centering of text. You will be asked to return an HTML file that will be used in an email. The resume you will be working on has already been formatted to the standardized format for the company it is being submitted to. This is a SaaS product.


Things that must be bold:
```
All of the sections titles:
-"Position Recommended"
-"Personal Information"
-"Educational Background"
-"Personal Information"
-"Assessment on Candidate"
-"Professional Experience"
-"Compensation"

Mischallaneous:
-The "End of Profile" text at the very bottom
-Everything inside the Personal Information section
-Everything inside the Educational Background section
-The date, company name, and job for every new experience inside the Experience section
-The word "Responsibilities" in the experience section
```
Nothing else should be bold.


Everything that should be font size 16:
```
All of the sections titles:
-"Position Recommended"
-"Personal Information"
-"Educational Background"
-"Personal Information"
-"Assessment on Candidate"
-"Professional Experience"
-"Compensation"

Mischallaneous:
-The "End of Profile" text at the very bottom
```
Everything else must be font size 12


Centering Text:
```
-The "End of Profile" text at the very bottom
```
Nothing else should be centered.


Critical Points:
```
-The actual words on the resume MUST stay the same, WORD FOR WORD. Do not summarize anything or change what the person said on the resume.
-There must be an empty line after every Section Title.
-There must be two empty lines before the end of a section and the start of a new Section.
-If a literal string character or ASCII character does not exist or will not render properly in HTML, replace it with an equivalent in html code.
-DO NOT ADD OR CHANGE THE CHARACTERS USED TO FORMAT THE RESUME. String literals such as ` - `, ` | ,`, `    , and even the number of newline characters` have been intentionally set to be a certain way, and must remain that way.
```


Return an html file.

""".strip()

















import re
import io
import json
import logging
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from email import policy
from email.parser import Parser
import pdfplumber
import fitz  # pymupdf


logger = logging.getLogger(__name__)


def simplify_email_object(obj):

    # returns a python dictionary where all the keys are strings,
    # and all the values are strings except for the key 'content',
    # which as a value of type 'bytes'

    def __parse_email_to_dict(email_raw: str):

        # Parse raw MIME email string
        msg = Parser(policy=policy.default).parsestr(email_raw)

        result = {
            "headers": dict(msg.items()),  # dict[str, str]
            "subject": msg.get("subject"),
            "from": msg.get("from"),
            "to": msg.get("to"),
            "text": None,
            "html": None,
            "attachments": []
        }

        # Walk through MIME parts
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))

            # Plain text body
            if content_type == "text/plain" and "attachment" not in content_disposition:
                result["text"] = part.get_content()

            # HTML body
            elif content_type == "text/html" and "attachment" not in content_disposition:
                result["html"] = part.get_content()

            # Attachments
            elif "attachment" in content_disposition:
                result["attachments"].append({
                    "filename": part.get_filename(),
                    "content_type": content_type,
                    "content": part.get_payload(decode=True)  # bytes
                })

        return result
    

    if not obj:
        return None

    email = None
    for k,v in obj.items():
        if "email" == k:
            email = __parse_email_to_dict(v)

    if not email:
        return None

    keep = ["to", "from", "subject", "sender_ip", "envelope"]
    obj = {k:v for k,v in obj.items() if k in keep}

    obj["email_text"] = email["text"]
    obj["email_html"] = email["html"]
    obj["attachments"] = email["attachments"]

    for k,v in obj.items():
        if type(v) == str:
            obj[k] = v.strip()

    att = None
    for k,v in obj.items():
        if k != "attachments":
            pass
        else:
            if len(v) >= 1:
                for attachment in v:
                    att = attachment
                    break
    
    # attachment_keys = ["filename", "content_type", "content"] # The ones I want to keep
    if not att:
        att = {}
        att["filename"] = ""
        att["content_type"] = ""
        att["content"] = ""

    else:
        obj["filename"] = att["filename"]
        obj["content_type"] = att["content_type"]
        obj["content"] = att["content"]

    from_name = ""
    from_email = ""

    try:
        obj["from_name"] = from_name
        obj["from_email"] = json.loads(obj["envelope"])["from"]
    except Exception as e:
        print(e)

    if not obj["from_email"]:
        try:
            from_email = "<".split(obj["frmo"][1].split(">")[0].strip())
            obj["from_email"] = from_email
        except Exception as e:
            print(e)

    return obj


def extract_text(filename: str, file_bytes: bytes, email_from: str) -> str:

    ext = filename.rsplit(".", 1)[-1].lower()

    print("ext", ext)
    # ONLY .txt
    if ext == 'txt':
        return file_bytes.decode("utf-8", errors="replace")

    # and .pdf supported
    if ext != "pdf":
        # Only doing PDFs at the moment
        return ""
    
    extracted_text = None
    excepted = False
    error_message = ""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        extracted_text = "\n".join(
            page.get_text("text") or "\n[MISSING_PAGE]\n" for page in doc
        )
    except Exception as e:
        excepted = True
        error_message += str(e) + ". | \n"


    if (extracted_text == None) or (excepted == True) or ("[MISSING_PAGE]" in extracted_text):
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                extracted_text = "\n".join(
                    page.extract_text() or "\n[MISSING_PAGE]\n" for page in pdf.pages
                )
        except Exception as e:
            excepted = True
            error_message += str(e) + ". | \n"


    if extracted_text and ("[MISSING_PAGE]" in extracted_text):
        return ""
        
    if (extracted_text == None):
        return ""
           
    return extracted_text


def detect_language(text: str) -> str:
    non_ws = [c for c in text if not c.isspace()]
    if not non_ws:
        return "en"
    cjk = sum(1 for c in non_ws if '\u4e00' <= c <= '\u9fff')
    return "zh" if (cjk / len(non_ws)) > 0.10 else "en"


def fix_response(resp: str) -> str:
    lines = resp.split("\n")
    lines = [line for line in lines if line.strip() != "```"]
    new_lines = []
    for i in range(len(lines)):
        date = False
        if lines[i].find("- ") == 0:
            temp = "- ".join(lines[i].split("- ")[1:])
            if temp and temp[0] in "0123456789" and temp[1] in "0123456789":
                if " | " in temp:
                    datee = temp.split(" | ")[0].strip()
                    if " - " in datee:                        
                        date = True
                

        if date == True:
            fixed = "- ".join(lines[i].split("- ")[1:])
            if fixed and fixed[0] == " ":
                fixed = fixed[1:]
            if fixed and fixed[0] == " ":
                fixed = fixed[1:]
            new_lines.append(fixed)
        else:
            if lines[i].find(" | ") == 0:
                new_lines.append(" | ".join(lines[i].split(" | ")[1:]))
            elif lines[i].find(" ") == 0:
                space_count = 0
                for j in range(len(lines[i])):
                    if lines[i][j] != " ":
                        break
                    else:
                        space_count += 1

                if space_count >= 4:
                    #intentional spaces
                    new_lines.append(lines[i])
                else:

                    #new_lines.append(lines[i][space_count:])
                    new_lines.append(lines[i]) ####

            else:
                new_lines.append(lines[i])


    return "\n".join(new_lines)


def create_local_docx_document(filename, extracted_text):
    
        
    doc = Document()

    def edit_distance(word1: str, word2: str) -> int:
        word1 = "-" + word1
        word2 = "-" + word2
        m = len(word1)
        n = len(word2)

        # Initialize the dp table
        dp = [[0] * (n) for _ in range(m)]

        # Base cases
        for i in range(m):
            dp[i][0] = i
        for j in range(n):
            dp[0][j] = j

        # Fill in the dp table
        for i in range(1, m):
            for j in range(1, n):
                if word1[i] == word2[j]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j-1], dp[i][j-1], dp[i-1][j])
        return dp[m-1][n-1]


    def __is_section_title(line):
        words = line.strip().split(" ")
        words = [word.strip() for word in  words if word.strip()]
        if len(words) > 3:
            return False
        if len(words) < 1:
            return False
        line = " ".join(words)
        titles = ["Position Recommended:", "Personal Information:", "Educational Background:", "Education Background:", "Personal Information:", "Assessment on Candidate:", "Professional Experience:", "Compensation:"]
        
        for title in titles:
            if line == title:
                return True
        
        return False


    for line in extracted_text.split("\n"):
        if line.strip().lower() == "end of profile":
            end_paragraph = doc.add_paragraph()
            end_run = end_paragraph.add_run(line)
            end_run.font.name = "Arial"
            end_run.font.size = Pt(12)
            end_run.bold = True
            end_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            break

        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        run = paragraph.add_run(line)
        run.font.name = "Arial"
        if __is_section_title(line):
            run.font.size = Pt(12)
            run.bold = True
            run.underline = True
        else:
            run.font.size = Pt(10)
            if line.strip().lower() in ["current salary:", "salary expectation:"]:
                run.bold = False
            else:
                run.bold = not line.startswith("- ")

    docx_filename = ".".join(filename.split(".")[:-1]) + ".docx"
    docx_filename = re.sub(" ", "_", docx_filename)
    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer, docx_filename


def create_local_docx_document_zh(filename, text):
    doc = Document()

    for line in text.split("\n"):
        is_bold = "[BOLD]" in line
        is_underline = "[UNDERLINE]" in line
        clean_line = line.replace("[BOLD]", "").replace("[UNDERLINE]", "")

        if clean_line.strip().lower() == "end of profile":
            end_paragraph = doc.add_paragraph()
            end_run = end_paragraph.add_run(clean_line.strip())
            end_run.font.name = "SimSun"
            end_run.font.size = Pt(12)
            end_run.bold = True
            end_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            rPr = end_run._element.get_or_add_rPr()
            rPr.get_or_add_rFonts().set(qn('w:eastAsia'), 'SimSun')
            break

        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        run = paragraph.add_run(clean_line)
        run.font.name = "SimSun"
        run.font.size = Pt(10)
        run.bold = is_bold
        run.underline = is_underline
        rPr = run._element.get_or_add_rPr()
        rPr.get_or_add_rFonts().set(qn('w:eastAsia'), 'SimSun')

    docx_filename = ".".join(filename.split(".")[:-1]) + ".docx"
    docx_filename = re.sub(" ", "_", docx_filename)
    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer, docx_filename


def get_form_dict(form):
    """
    Convert FastAPI / Starlette FormData → JSON string
    """

    form_dict = {}

    for key in form.keys():
        values = form.getlist(key)

        if len(values) == 1:
            value = values[0]
        else:
            value = values

        if hasattr(value, "filename"):
            value = {
                "filename": value.filename,
                "content_type": value.content_type,
            }

        elif isinstance(value, list):
            new_list = []

            for v in value:
                if hasattr(v, "filename"):
                    new_list.append({
                        "filename": v.filename,
                        "content_type": v.content_type,
                    })
                else:
                    new_list.append(v)

            value = new_list

        form_dict[key] = value

    form_json = json.dumps(form_dict, indent=2)

    return form_json
















import os
import io
import time
import json
import base64
import logging
import uuid
import secrets
from datetime import datetime

import openai
from openai import OpenAI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

import sendgrid
from sendgrid import SendGridAPIClient
from twilio.rest import Client as TwilioClient
from sendgrid.helpers.mail import (
    Mail, ReplyTo, Attachment, FileContent, FileName,
    FileType, Disposition
)


# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
print(os.path.join(os.path.dirname(__file__), ".env"))



#### 
OPENAI_API_KEY="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"

#### EMAIl
SENDGRID_API_KEY="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"

#### TWILIO / ACCOUNT MANAGING MOSTLY PHONE
TWILIO_ACCOUNT_SID="AC98b70f32a7e74ce8466d5f118bfe8d3e"
TWILIO_AUTH_TOKEN="0937e0017b79dd2645a5caec93e5f096"
#### NOT THE RIGHT DB URL
SQLALCHEMY_DATABASE_URI="postgresql://postgres.pmzfpumwwclgtvkfapqa:DatabasePasswordat123@aws-1-us-east-1.pooler.supabase.com:5432/postgres"



openai.api_key = OPENAI_API_KEY
openai_client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger(__name__)


def get_llm_info(transcript_json):
    if not transcript_json or transcript_json == "[]" or transcript_json == "None":
        return "N/A", "N/A"

    try:
        messages = json.loads(transcript_json)
        transcript_text = ""
        for m in messages:
            role = m.get('role', 'unknown')
            content = m.get('content', '')
            transcript_text += f"{role}: {content}\n"

        if not transcript_text.strip():
            return "N/A", "N/A"

        prompt = f"""You are summarizing a voice call handled by an AI receptionist on behalf of a business.

Transcript:
{transcript_text}

Extract the following and return as JSON:

1. "full_name": The caller's full name if they stated it, otherwise "N/A".

2. "summary": A detailed 3–5 sentence summary of the interaction. Include ALL of the following that were mentioned:
   - Why the caller called and what they were looking for
   - The specific service, treatment, or inquiry (e.g. haircut type, legal matter, medical question, booking request)
   - The name of any staff member, provider, lawyer, barber, doctor, etc. requested or assigned
   - Any date, time, or scheduling details (e.g. "today at 6 PM", "Thursday at 2 PM")
   - Any pricing or deposit information discussed
   - The outcome of the call (e.g. appointment booked, information provided, callback requested, issue unresolved)
   - Any next steps or follow-up actions mentioned

Write the summary in plain past-tense prose as if briefing a manager who was not on the call. Be specific - do not omit names, times, or services that were mentioned.

Return only valid JSON:
{{
    "full_name": "...",
    "summary": "..."
}}"""

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        full_name = result.get("full_name", "N/A")
        summary = result.get("summary", "N/A")

        try:
            #### Fix bug for one account specifically
            import re
            summary = re.sub("Jeffrey Horace", "Jeffrey Horrick", summary)
            summary = re.sub("Jeffrey Horak", "Jeffrey Horrick", summary)
            summary = re.sub("Jeffrey Horaquez", "Jeffrey Horrick", summary)
            ####
        except:
            pass
        return full_name, summary
        #return result.get("full_name", "N/A"), result.get("summary", "N/A")
    except Exception as e:
        logger.info(f"Error in LLM extraction: {e}")
        return "N/A", "N/A"


def ask_GPT(query: str, model="gpt-4o") -> str:
    ans = None
    try:
        response = openai_client.chat.completions.create(
            model=model,
            max_completion_tokens=12000,
            messages=[{"role": "user", "content": query}]
        )
        ans = response.choices[0].message.content.strip()
    except Exception as e:
        logger.info("\nError Occured when making request to OpenAI:")
        logger.info(e)
        logger.info("Sleeping for 10 seconds due to error")
        time.sleep(10)
    return ans


def send_email(to_email, subject, html_content):

    def __send_email(to_email, subject, html_content):
        message = Mail(
            from_email="agent@standardhc.info",
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        message.reply_to = ReplyTo("bilan604gm@gmail.com", "Bill")

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Status code: {response.status_code}")
        return response.status_code
    
    # Example execution
    status_code = __send_email(
        to_email=to_email,
        subject=subject,
        html_content=html_content
    )

    return status_code


def send_sms(from_number: str, to_number: str, body: str) -> str:
    client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(body=body, from_=from_number, to=to_number)
    return message.sid


def send_email_with_attatchment(to_emails: str, subject: str, html_content: str, filename: str, filepath: list[str] = [], from_email: str = "agent@standardhc.hk", buffer=None):
    # sends email with a file attatchment using sendgrid
    # filepath: use list of folder names, don't include the "/"'s 
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

    buffer.seek(0)
    file_data = base64.b64encode(buffer.read()).decode()
        
    attachment = Attachment(
        FileContent(file_data),
        FileName(filename),
        FileType("application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        Disposition("attachment")
    )

    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content
    )
    message.attachment = attachment

    response = sg.send(message)
    return response


def format_email_with_ai_and_send(EMAIL_OBJECT: dict, extracted_text: str):

    lang = detect_language(extracted_text)

    if lang == "zh":
        prompt_1 = NEW_RESUME_FORMATTING_PROMPT_1_ZH.replace("{{{INPUT}}}", extracted_text)
        response_1 = ask_GPT(prompt_1)
        response_1 = "\n".join(line for line in response_1.split("\n") if line.strip() != "```")
        print(f"\n\n------------->\nresponse_1 generated:\n{response_1[:min(len(response_1), 1000)]}\n")
        buffer, docx_filename = create_local_docx_document_zh(EMAIL_OBJECT["filename"], response_1)
    else:
        prompt_1 = RESUME_FORMATTING_PROMPT_1.replace("{{{INPUT}}}", extracted_text)
        response_1 = ask_GPT(prompt_1)
        print(f"\n\n------------->\nresponse_1 generated:\n{response_1[:min(len(response_1), 1000)]}\n")
        fixed_resume = fix_response(response_1)
        print(f"\n\n--------------->\nfixed_resume for ({EMAIL_OBJECT['filename']}\n{fixed_resume[:min(len(fixed_resume), 1000)]}\n")
        buffer, docx_filename = create_local_docx_document(EMAIL_OBJECT["filename"], fixed_resume)

    print(f"\n\n--------------->\nlocal_docx_filename:\n{docx_filename}\n")

    send_to_email = json.loads(EMAIL_OBJECT["envelope"])["from"]
    subject = f'Formatted Resume: {EMAIL_OBJECT["filename"]}'
    email_html_content = f"Attatchment for {EMAIL_OBJECT['filename']}. (response from agent@standardhc.hk)"

    status_code = send_email_with_attatchment(
        to_emails=send_to_email,
        subject=subject,
        html_content=email_html_content,
        filename=docx_filename,
        filepath=[],
        from_email="agent@standardhc.info",
        buffer=buffer
    )
    print("Send email status code:", status_code)

    return {"status": "success"}


def handle_standardhc_workflow(filename):

    obj = None
    
    with open(filename, "r", encoding="utf-8") as f:
            content = f.readlines()
            content = "".join(content)
            obj = json.loads(content)
    
    obj = simplify_email_object(obj)
    print("obj keys:", list(obj.keys()))

    EMAIL_OBJECT = obj

    extracted_text = extract_text(obj["filename"], obj["content"], obj["from_email"])
    print(f"extracted_text:\n{extracted_text}")

    format_email_with_ai_and_send(EMAIL_OBJECT, extracted_text)


app = FastAPI()

def _process_inbound_email(form_json: str, filename: str):
    try:
        with open(filename, "w+", encoding="utf-8") as f:
            f.write(form_json)
        handle_standardhc_workflow(filename)
    except Exception as e:
        logger.error(f"ERROR in background _process_inbound_email: {str(e)}")


@app.post("/inbound-email/")
async def shc_inbound_email(request: Request, background_tasks: BackgroundTasks):
    logger.info("SHC /inbound-email/ received")
    try:
        form = await request.form()
    except Exception as e:
        logger.error(f"Failed to parse form: {e}")
        return {"status": "ok"}

    try:
        form_json = get_form_dict(form)
        filename = "shc_form_dump.json"
        background_tasks.add_task(_process_inbound_email, form_json, filename)
    except Exception as e:
        logger.error(f"Failed to enqueue email processing: {e}")

    return {"status": "ok"}

@app.get("/ping/")
def ping():
    return {"message": "Reached"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
