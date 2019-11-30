import re

from hata import eventlist, ChannelText, CHANNELS

from cbmodules import config

commands = eventlist()

UNFILTERED_CHANNEL = ChannelText.precreate(637949482784260124)
STOP_CROSS_RP = re.compile('/remove-link', re.I)

@commands(case='add-link')
async def add_link(client, message, content):
    # owner check or such?
    try:
        await config.CROSSLINK_IDS.append(message.channel.id, raise_=True)
    except ValueError:
        content = 'Channel is already in the CrossLink network!'
    else:
        client.events.message_create.append(Crossposter(client),message.channel)
        content = f'Added {message.channel:m} to CrossLink Network!'

    await client.message_create(message.channel, content)
                
@commands(case='remove-link')
async def remove_link(client, message, content):
    # owner check or such?
    try:
        await config.CROSSLINK_IDS.remove(message.channel.id,raise_=True)
    except ValueError:
        content = 'Channel isn\'t in the CrossLink network.'
    else:
        client.events.message_create.remove(Crossposter(client),message.channel)
        content = f'Removed {message.channel:m} from CrossLink Network'

    await client.message_create(message.channel, content)
    

@commands(case='get-links')
async def get_links(client, message, content):
    if config.CROSSLINK_IDS:
        content = '\n'.join(f'- {channel_id}' for channel_id in config.CROSSLINK_IDS)
    else:
        content = 'No channels are currently CrossLinked!'

    await client.message_create(message.channel, content)

class Crossposter(object):
    __slots__ = ('client', )
    
    def __init__(self, client):
        self.client = client

    async def __call__(self, message):
        client = self.client
        
        if (message.author is self.client) and (message.channel is UNFILTERED_CHANNEL):
            channels = []
            for channel_id in config.CROSSLINK_IDS:
                channel = CHANNELS[channel_id]
                if channel is UNFILTERED_CHANNEL:
                    continue
                
                channels.append(channel)

            if not channels:
                return
            
            content = message.clean_content
            if not content:
                return

            for channel in channels:
                client.loop.create_task(client.message_create(channel, content))
                        
            return

        if message.author.is_bot:
            return

        if STOP_CROSS_RP.fullmatch(message.content):
            return

        channels=[]
        ignore_id=message.channel.id
        for channel_id in config.CROSSLINK_IDS:
            if channel_id==ignore_id:
                continue
            
            channel = CHANNELS[channel_id]
            channels.append(channel)

        if not channels:
            return

        content=message.clean_content
        if not content:
            return
        
        content=f'**{message.guild.name}**-{message.author:f}:\n{content}'

        for channel in channels:
            client.loop.create_task(client.message_create(channel, content))
        
    def __eq__(self,other):
        if type(self) is not type(other):
            return NotImplemented

        return (self.client is other.client)

async def channel_delete(client, channel):
    if channel.id not in config.CROSSLINK_IDS:
        return
    
    client.events.message_create.remove(Crossposter(client),channel)
    
    await config.CROSSLINK_IDS.remove(channel.id)
    
async def entry(client):
    client.events(channel_delete)
    
    if not config.CROSSLINK_IDS:
        return

    channels=[]
    to_delete=[]
    for channel_id in config.CROSSLINK_IDS:
        try:
            channel = CHANNELS[channel_id]
        except KeyError:
            # the channel is deleted, lets remove it
            to_delete.append(channel_id)
        else:
            channels.append(channel)
    channel = CHANNELS[637949482784260124]
    channels.append(channel)
    
    if to_delete:
        await config.CROSSLINK_IDS.remove_multiple(to_delete)
        
    CROSSPOSTER = Crossposter(client)
    event=client.events.message_create
    
    for channel in channels:
        event.append(CROSSPOSTER, channel)
            

def exit(client):
    del client.events.channel_delete
    
    if not config.CROSSLINK_IDS:
        return

    CROSSPOSTER = Crossposter(client)
    event=client.events.message_create
    
    channels=[]
    for channel_id in config.CROSSLINK_IDS:
        channel=CHANNELS[channel_id]
        channels.append(channel)
    
    for channel in channels:
        event.remove(CROSSPOSTER, channel)



