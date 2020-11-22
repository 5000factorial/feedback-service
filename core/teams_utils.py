def app_manifest(website_url, privacy_url, tos_url, configuration_url, valid_domains):
    return {
        "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.8/MicrosoftTeams.schema.json",
        "manifestVersion": "1.8",
        "version": "1.0.0",
        "id": "f2f78c7b-15a7-4ef6-94f0-84dc4f9eb5e7",
        "packageName": "ru.spbu.feedback-service",
        "developer": {
            "name": "Saint Petersburg University",
            "websiteUrl": website_url,
            "privacyUrl": privacy_url,
            "termsOfUseUrl": tos_url,
        },
        "icons": {
            "color": "color.png",
            "outline": "outline.png"
        },
        "name": {
            "short": "Feedback Service",
            "full": "Feedback Service"
        },
        "description": {
            "short": "Saint Petersburg State University Feedback Service",
            "full": "Saint Petersburg State University Feedback Service"
        },
        "accentColor": "#FFFFFF",
        "configurableTabs": [
        {
            "configurationUrl": configuration_url,
            "canUpdateConfiguration": True,
            "scopes": ["team", "groupchat"],
            "context": [
                "channelTab",
                "privateChatTab",
            ],
            "supportedSharePointHosts": [
            "sharePointFullPage",
            "sharePointWebPart"
            ]
        }
        ],
        "permissions": [
        "identity",
        "messageTeamMembers"
        ],
        "validDomains": valid_domains
    }