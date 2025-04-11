"""Reolink Baichuan XML templates."""

XML_HEADER = """<?xml version="1.0" encoding="UTF-8" ?>
"""

LOGIN_XML = """<?xml version="1.0" encoding="UTF-8" ?>
<body>
<LoginUser version="1.1">
<userName>{userName}</userName>
<password>{password}</password>
<userVer>1</userVer>
</LoginUser>
<LoginNet version="1.1">
<type>LAN</type>
<udpPort>0</udpPort>
</LoginNet>
</body>
"""

LOGOUT_XML = """<?xml version="1.0" encoding="UTF-8" ?>
<body>
<LoginUser version="1.1">
<userName>{userName}</userName>
<password>{password}</password>
<userVer>1</userVer>
</LoginUser>
</body>
"""

CHANNEL_EXTENSION_XML = """<?xml version="1.0" encoding="UTF-8" ?>
<Extension version="1.1">
<channelId>{channel}</channelId>
</Extension>
"""

DingDongOpt_1_XML = """
<?xml version="1.0" encoding="UTF-8" ?>
<body>
<dingdongDeviceOpt version="1.1">
<opt>delDevice</opt>
<id>{chime_id}</id>
</dingdongDeviceOpt>
</body>
"""

DingDongOpt_2_XML = """
<?xml version="1.0" encoding="UTF-8" ?>
<body>
<dingdongDeviceOpt version="1.1">
<id>{chime_id}</id>
<opt>getParam</opt>
</dingdongDeviceOpt>
</body>
"""

DingDongOpt_3_XML = """
<?xml version="1.0" encoding="UTF-8" ?>
<body>
<dingdongDeviceOpt version="1.1">
<opt>setParam</opt>
<id>{chime_id}</id>
<volLevel>{vol}</volLevel>
<ledState>{led}</ledState>
<name>{name}</name>
</dingdongDeviceOpt>
</body>
"""

DingDongOpt_4_XML = """
<?xml version="1.0" encoding="UTF-8" ?>
<body>
<dingdongDeviceOpt version="1.1">
<id>{chime_id}</id>
<opt>ringWithMusic</opt>
<musicId>{tone_id}</musicId>
</dingdongDeviceOpt>
</body>
"""

SetDingDongCfg_XML = """
<?xml version="1.0" encoding="UTF-8" ?>
<body>
<dingdongCfg version="1.1">
<deviceCfg>
<id>{chime_id}</id>
<alarminCfg>
<valid>{state}</valid>
<musicId>{tone_id}</musicId>
<type>{event_type}</type>
</alarminCfg>
</deviceCfg>
</dingdongCfg>
</body>
"""

QuickReplyPlay_XML = """
<?xml version="1.0" encoding="UTF-8" ?>
<body>
<audioFileInfo version="1.1">
<channelId>{channel}</channelId>
<id>{file_id}</id>
<timeout>0</timeout>
</audioFileInfo>
</body>
"""

SetRecEnable = """
<?xml version="1.0" encoding="UTF-8" ?>
<body>
<Record version="1.1">
<channelId>{channel}</channelId>
<enable>{enable}</enable>
</Record>
</body>
"""

SetPrivacyMode = """
<?xml version="1.0" encoding="UTF-8" ?>
<body>
<sleepState version="1.1">
<operate>2</operate>
<sleep>{enable}</sleep>
</sleepState>
</body>"""

GetSceneInfo = """
<?xml version="1.0" encoding="UTF-8" ?>
<body>
<sceneCfg version="1.1">
<id>{scene_id}</id>
</sceneCfg>
</body>"""

DisableScene = """
<?xml version="1.0" encoding="UTF-8" ?>
<body>
<sceneModeCfg version="1.1">
<enable>0</enable>
</sceneModeCfg>
</body>"""

SetScene = """
<?xml version="1.0" encoding="UTF-8" ?>
<body>
<sceneModeCfg version="1.1">
<enable>1</enable>
<curSceneId>{scene_id}</curSceneId>
</sceneModeCfg>
</body>"""
