import asyncio
import aiohttp
import json

# ------------------------------------------------------------------------------
async def get_subreddits(subreddits, limit=50, min_score=5000):
    '''Gets the top threads (up to the given limit and minimum score) for the
    given list of subreddits.

    Parameters
    ----------
        subreddits (list). List of strings with the names of the subreddits to
        query the top threads for.

        limit (int). Maximum number of threads to query the server, to constrain
        the load on the server and the communication link. The default is 50 and
        the minimum acceptable is 1.

        min_score (int). The minimum score for a thread to be considered as top
        (besides the reddit original indication from the top query). The default
        is 5000 and the minimum acceptable is 0.

    Returns
    -------
        data (list). A list of dictionaries containing the top threads for each
        subreddit given in the `subreddits` argument. Each item in the list is a
        dictionary containing the following attributes:
            {
                'subreddit': 'name of the subreddit',
                'threads': [ list of dictionaries with thread data ]
            }
        For details on the contents of the list of dictionaries in the `threads`
        attribute, please refer to the return type in the documentation of 
        function `_get_top_threads`.
    '''
    limit = max(limit, 1)
    min_score = max(min_score, 0)

    data = []
    client = aiohttp.ClientSession(loop=asyncio.get_event_loop())

    for subreddit in subreddits:
        sub_data = await _get_top_threads(client, subreddit, limit, min_score)        
        data.append({
            'subreddit': subreddit,
            'threads': sub_data
        })

    await client.close()
    return data

# ------------------------------------------------------------------------------
async def _get_top_threads(client, subreddit, limit, min_score):
    '''Gets the top threads (up to the given limit and minimum score) for the
    given subreddit.

    Parameters
    ----------
        client (aiohttp.ClientSession). A HTTP asynchronous session previously
        opened and running in the same event loop of this call, to be used to
        query the JSON data from the reddit server.

        subreddit (str). Name of the subreddit to query the top threads for.

        limit (int). Maximum number of threads to query the server, to constrain
        the load on the server and the communication link.

        min_score (int). The minimum score for a thread to be considered as top
        (besides the reddit original indication from the top query).

    Returns
    -------
        data (list). A list of dictionaries containing the top threads for the
        given subreddit. Each item in the list is a dictionary containing the
        following attributes:
            {
                'url': 'string of the thread url',
                'title': 'string of the thread title',
                'score': integer of the thread score,
                'ups': integer of the number of up votes in the thread,
                'downs': integer of the number of down votes in the thread,
                'author': 'string of the thread's author name',
                'num_comments': integer of the number of comments in the thread,
                'url_comments': 'string of the thread comments url'
            }
    '''
    # Setup the base and query url
    base_url = 'https://old.reddit.com'
    query = f'top.json?sort=top&t=day&limit={limit}'
    url = f'{base_url}/r/{subreddit}/{query}'
    
    # Get the JSon data from the URL
    async with client.get(url) as query_response:
        assert query_response.status == 200
        json_resp = await query_response.read()
        response = json.loads(json_resp.decode('utf-8'))

    # Build the dictionary data to return
    data = []
    for resp in response['data']['children']:
        if min_score > 0 and resp['data']['score'] < min_score:
            break

        item = {
            'url': resp['data']['url'],
            'title': resp['data']['title'],
            'score': resp['data']['score'],
            'ups': resp['data']['ups'],
            'downs': resp['data']['downs'],
            'author': resp['data']['author'],
            'num_comments': resp['data']['num_comments'],
            'url_comments': base_url + resp['data']['permalink']
        }
        data.append(item)

    return data