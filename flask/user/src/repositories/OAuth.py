import json

from config import config
from rauth import OAuth2Service

from flask import redirect, request


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        self.consumer_id = config.oauth_vk.client_id[0]
        self.consumer_secret = config.oauth_vk.client_secret[0]

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return config.oauth_vk.CALLBACK_URL[0]

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class VkontakteSignIn(OAuthSignIn):
    def __init__(self):
        super(VkontakteSignIn, self).__init__("Vkontakte")
        self.service = OAuth2Service(
            name=config.oauth_vk.name,
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url=config.oauth_vk.authorize_url[0],
            access_token_url=config.oauth_vk.access_token_url[0],
            base_url=config.oauth_vk.base_url[0],
        )

    def authorize(self):
        return redirect(
            self.service.get_authorize_url(
                redirect_uri=self.get_callback_url(),
                scope="email",
                response_type="code",
                v=5.131,
            )
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode("utf-8"))

        if "code" not in request.args:
            return None, None, None

        data_post = {
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": self.get_callback_url(),
        }

        oauth_session = self.service.get_auth_session(
            data=data_post, decoder=decode_json
        )
        return json.loads(oauth_session.access_token_response.text)
