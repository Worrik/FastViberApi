from typing import Optional, List, Any, Union, Callable
from typing_extensions import Literal

from pydantic import BaseModel


class BotConfiguration(BaseModel):
    auth_token: str
    name: str
    avatar: Optional[str]


class Webhook(BaseModel):
    url: str
    event_types: List = [
        "delivered",
        "seen",
        "failed",
        "subscribed",
        "unsubscribed",
        "conversation_started"
    ]
    send_name: bool = True
    send_photo: bool = True


class User(BaseModel):
    id: Optional[str]
    name: Optional[str]
    avatar: Optional[str]
    country: Optional[str]
    language: Optional[str]
    api_version: Optional[int]


class BaseRequest(BaseModel):
    event: str
    answer: Callable = None


class WebhookRequest(BaseRequest):
    event: Literal['webhook']
    timestamp: int
    message_token: int


class SubscribedRequest(BaseRequest):
    event: Literal['subscribed']
    timestamp: Optional[int]
    user: Optional[User]
    message_token: Optional[int]
    chat_hostname: Optional[str]


class UnsubscribedRequest(BaseRequest):
    event: Literal['unsubscribed']
    timestamp: Optional[int]
    user_id: Optional[str]
    message_token: Optional[int]
    chat_hostname: Optional[str]


class ConversationStartedRequest(BaseRequest):
    event: Literal['conversation_started']
    timestamp: Optional[int]
    message_token: Optional[int]
    type: Optional[str]
    context: Optional[str]
    user: Optional[User]
    subscribed: Optional[bool]
    chat_hostname: Optional[str]


class DeliveredRequest(BaseRequest):
    event: Literal['delivered']
    timestamp: Optional[int]
    message_token: Optional[int]
    user_id: Optional[str]
    chat_hostname: Optional[str]


class SeenRequest(BaseRequest):
    event: Literal['seen']
    timestamp: Optional[int]
    message_token: Optional[int]
    user_id: Optional[str]
    chat_hostname: Optional[str]


class FailedRequest(BaseModel):
    event: Literal['failed']
    timestamp: Optional[int]
    message_token: Optional[int]
    user_id: Optional[str]
    desc: Optional[str]
    chat_hostname: Optional[str]


class Sender(BaseModel):
    id: Optional[str]
    name: Optional[str]
    avatar: Optional[str]
    country: Optional[str]
    language: Optional[str]
    api_version: Optional[int]


class InternalBrowser(BaseModel):
    ActionButton: Optional[str]
    ActionPredefinedURL: Optional[str]
    TitleType: Optional[str]
    CustomTitle: Optional[str]
    Mode: Optional[str]
    FooterType: Optional[str]
    ActionReplyData: Optional[str]


class Map(BaseModel):
    Latitude: Optional[str]
    Longitude: Optional[str]


class Frame(BaseModel):
    BorderWidth: Optional[str]
    BorderColor: Optional[str]
    CornerRadius: Optional[str]


class MediaPlayer(BaseModel):
    Title: Optional[str]
    Subtitle: Optional[str]
    ThumbnailURL: Optional[str]
    Loop: Optional[bool]


class Button(BaseModel):
    Columns: Optional[int]
    Rows: Optional[int]
    BgColor: Optional[str]
    Silent: Optional[bool]
    BgMediaType: Optional[str]
    BgMedia: Optional[str]
    BgMediaScaleType: Optional[str]
    ImageScaleType: Optional[str]
    BgLoop: Optional[bool]
    ActionType: Optional[str]
    ActionBody: Optional[str]
    Image: Optional[str]
    Text: Optional[str]
    TextVAlign: Optional[str]
    TextHAlign: Optional[str]
    TextPaddings: Optional[str]
    TextOpacity: Optional[int]
    TextSize: Optional[str]
    OpenURlType: Optional[str]
    OpenURLMediaType: Optional[str]
    TextBgGradientColor: Optional[str]
    TextShouldFit: Optional[bool]
    TextSize: Optional[str]
    InternalBrowser: Optional[InternalBrowser]
    Map: Optional[Map]
    Frame: Optional[Frame]
    MediaPlayer: Optional[MediaPlayer]


class FavoritesMetadata(BaseModel):
    type: Optional[str]
    url: Optional[str]
    title: Optional[str]
    thumbnail: Optional[str]
    domain: Optional[str]
    width: Optional[int]
    height: Optional[int]
    alternativeUrl: Optional[str]
    alternativeText: Optional[str]


class Keyboard(BaseModel):
    Type = 'keyboard'
    Buttons: Optional[List[Button]]
    BgColor: Optional[str]
    DefaultHeight: Optional[bool]
    CustomDefaultHeight: Optional[int]
    HeightScale: Optional[int]
    ButtonsGroupColumns: Optional[int]
    ButtonsGroupRows: Optional[int]
    InputFieldState: Optional[str]
    FavoritesMetadata: Optional[FavoritesMetadata]


class BaseMessage(BaseModel):
    keyboard: Optional[dict]


class Message(BaseMessage):
    type: Literal['text'] = 'text'
    text: Optional[str]
    sender: Optional[Sender]
    tracking_data: Optional[Any]
    min_api_version: Optional[int]


class PictureMessage(BaseMessage):
    type: Literal['picture'] = 'picture'
    media: Optional[str]
    thumbnail: Optional[str]


class VideoMessage(BaseMessage):
    type: Literal['video'] = 'video'
    media: Optional[str]
    size: Optional[int]
    duration: Optional[int]
    thumbnail: Optional[str]


class FileMessage(BaseMessage):
    type: Literal['file'] = 'file'
    media: Optional[str]
    size: Optional[int]
    file_name: Optional[str]


class Contact(BaseModel):
    name: Optional[str]
    phone_number: Optional[str]


class ContactMessage(BaseMessage):
    type: Literal['contact'] = 'contact'
    contact: Optional[Contact]


class Location(BaseModel):
    lat: Optional[str]
    lon: Optional[str]


class LocationMessage(BaseMessage):
    type: Literal['location'] = 'location'
    location: Optional[Location]


class URLMessage(BaseMessage):
    type: Literal['url'] = 'url'
    media: Optional[str]


class StickerMessage(BaseMessage):
    type: Literal['sticker']
    sticker_id: Optional[int]


class RichMedia(BaseModel):
    ButtonsGroupColumns: Optional[int] = 6
    ButtonsGroupRows: Optional[int] = 6
    Buttons: Optional[List[Button]]


class RichMediaMessage(BaseMessage):
    type: Literal['rich_media'] = 'rich_media'
    min_api_version: Optional[int]
    alt_text: Optional[str]
    rich_media: Optional[RichMedia]


class ReceiveMessageRequest(BaseRequest):
    event: Literal['message']
    timestamp: Optional[int]
    message_token: Optional[int]
    sender: Optional[Sender]
    message: Union[
        Message, PictureMessage, VideoMessage,
        FileMessage, ContactMessage, LocationMessage,
        URLMessage, StickerMessage, RichMediaMessage
    ]
    chat_hostname: Optional[str]


viber_request = Union[WebhookRequest, SubscribedRequest, UnsubscribedRequest,
                      ConversationStartedRequest, DeliveredRequest,
                      SeenRequest, FailedRequest, ReceiveMessageRequest]
