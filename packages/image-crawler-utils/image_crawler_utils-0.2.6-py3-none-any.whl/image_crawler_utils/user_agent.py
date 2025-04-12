import random



class UserAgent:

    pc_user_agents = {
        "Chrome - Windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Chrome - MAC": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Edge - Windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edge/18.17763", 
        "Safari 5.1 - MAC": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Safari 5.1 - Windows": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "IE 9.0": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
        "IE 8.0": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "IE 7.0": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "IE 6.0": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Firefox 4.0.1 - MAC": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Firefox 4.0.1 - Windows": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera 11.11 - MAC": "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera 11.11 - Windows": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Maxthon": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Tencent TT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "The World 2.x": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "The World 3.x": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "sogou 1.x": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "360": "MMozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Avant": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Green Browser": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    }


    mobile_user_agents = {
        "Chrome - iOS": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/31.0.1650.18 Mobile/11B554a Safari/8536.25",
        "Chrome - Android": "Mozilla/5.0 (Linux; Android 4.2.1; M040 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36",
        "iOS 4.33 - iPhone": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6553.18.5",
        "iOS 4.33 - iPod Touch": "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6553.18.5",
        "iOS 4.33 - iPad": "Mozilla/5.0 (iPad; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6553.18.5",
        "Android N1": "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Android QQ": "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Android Opera": "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "Android Pad Moto Xoom": "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Blackberry": "Mozilla/5.0 (Blackberry; U; Blackberry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "WebOS HP Touchpad": "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "Nokia N97": "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        "Windows Phone Mango": "Mozilla/4.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        "UC": "UCWEB7.0.2.37/28/999",
        "UC Standard": "NOKIA5700/UCWEB7.0.2.37/28/999",
        "UC Openwave": "Openwave/UCWEB7.0.2.37/28/999",
        "UC Opera": "Mozilla/4.0 (compatible; MSIE 6.0;) Opera/UCWEB7.0.2.37/28/999",
    }


    @property
    def user_agents():
        return {**UserAgent.pc_user_agents, **UserAgent.mobile_user_agents}
    

    def random_agent_with_name(header_type: str):
        """
        Select a random user agent with certain header_type.

        Parameters:
            header_type (str): The type of headers. e.g. "Chrome" will select randomly from "Chrome Windows", "Chrome MAC", etc.
        """

        random_key = random.choice([key for key in list({**UserAgent.pc_user_agents, **UserAgent.mobile_user_agents}.keys()) if header_type.lower() in key.lower()])
        return {'User-Agent': {**UserAgent.pc_user_agents, **UserAgent.mobile_user_agents}[random_key]}


    def random_pc_agent():
        """
        Select a random PC user agent.
        """

        random_key = random.choice(list(UserAgent.pc_user_agents.keys()))
        return {'User-Agent': UserAgent.pc_user_agents[random_key]}
    

    def random_mobile_agent():
        """
        Select a random mobile user agent.
        """

        random_key = random.choice(list(UserAgent.mobile_user_agents.keys()))
        return {'User-Agent': UserAgent.mobile_user_agents[random_key]}
    

    def random_agent():
        """
        Select a random user agent.
        """

        user_agents = UserAgent.user_agents
        random_key = random.choice(list(user_agents.keys()))
        return {'User-Agent': user_agents[random_key]}
    