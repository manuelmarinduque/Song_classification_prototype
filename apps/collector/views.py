from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.utils import IntegrityError

from .classes.collector import Collector
from spotipy.exceptions import SpotifyException
from .models import Artist, Song

# Create your views here.


def searchArtist(request):
    if request.method == 'POST':
        artist_uri = request.POST.get('artist_uri')
        return HttpResponseRedirect(reverse('collector:add_database_page', args=(artist_uri, )))
    else:
        return render(request, 'collector/search_artist.html')


def addDatabase(request, artist_uri):
    collector = Collector()

    artists = ('1QcwtcwAClkmeaVofZ4zUn','2AZOALDIBORfbzKTuliwdJ','5v287QKYZ7Dyuw4CNzv89p','44nb9BaqV2jVvxKCaXHwlP','7afXSXOa8dE3c2C5XIguAv','5lODCkFdEtpPn3YxfmyLfT','4EzD52bDFGZTEeEucKHtDs')
    # artists = ('3aeY1LxKK63GRg7tmI8UVa','5GNSVtCq2hiXDx7jUA5Iou','1c22GXH30ijlOfXhfLz9Df','2Z0C8UvMoiixS0cRV8Urtr','4SlusIRNswGYkTjhflokfX','54gCRV0IGOEsK5iZFjdKXo','3IUAZiICL3J7GlHYPgT414')
    # artists = ('3nlpTZci9O5W8RsNoNH559','4yNdrUaF54csrLixVTnqzC','5LCDv4TvYRQD5ehflOBEh4','6w1XCiB8efbfnusJ2jzmvu','0hD97064k3LBUrRvfT42SE','7wLYNBd1fXGEKSLJMNnlt4','2uYEU8bUQQ77Bk9HJJwxqx')
    # artists = ('1dI3emu3Tf6ZydmpCEZmqx','2wZmh2ddEInC5pzZ8O68lt','3tuushgEVJSXAkxR4ZxOhJ','4pv1Jo4PbYI8LMADJoTWjE','6biY6yyLVZzisjmFLx0AP1','6zk8WqI12buD0B67tteQ5h','2Otnykd696YidQYfEGVmNq')
    # artists = ('3MHaV05u0io8fQbZ2XPtlC','5lwmRuXgjX8xIwlnauTZIP','1qto4hHid1P71emI6Fd8xi','66NweiA3nU84k1S3SZdTSG','6n21XaDAuqpceTXBiypR9W','3vA0UcLmHZEoVavifm65mc','3yHLsTJ9OZ19qwY1Q5BEQJ')
    # artists = ('0P8EpsSMekkWtsX331Iebt','6dexNK5MjEL8UvmA5MjSgg','0VWoer2RDTKY4Sr9U93QTJ','3OcvS8PzSGYMBvLdzY6g3e','7rNbdH4pgrnwguvzxhA2Ek','36nvA2snEFUkDbg5qI0ZiG','0gudLEFCyMFIBCt1EQaMh7')
    # artists = ('0c59rGZvvhTT89vbLMiiM6','5p1D7KgsRRcS9gpQyRARrL','34zJjO7ns1qmMYJxJPF1wP','1viot8lL4r3cgRLb2hBUri','0B9fAbZMZTBXUyffDU2Mxj','1i2sOJlmgkWrWx28rB17Bd','1f6CQnTy4FKDgLGzp6G2Wd')
    # artists = ('1JzCCMAjM3FCr9eM3jp0uH','2pctdrQetn7EI0QpCm9RIF','7GMRarEViKQmiTUMFZtrfe','19ufHMEaPSvoM3iIVk8sTR','2w1UJL5kYJJkvjo71fQjOB','15g2N69hNuvVjSUqa9Entz','5CSek6ot4XS2AWiw1NFTiF')
    # artists = ('0xHOGt5gf3A1XJP79Zth9k','2O76CmUXGThMPPImBOnbUA','1aw0Cdl1DIrtUrUA6fGbAR','65HuWBUC1d8ty1q6J42Nfi','11wOrJLuakmQqTuhXXW2xz','3yyWIPmsesks6c7uMnvNn2','2ST5XwWB4uXGKk2NXP8DUI')
    # artists = ('7FnZWGw9lwOr7WzieTKEPR','7BfDn0T1IbJiD0U8j27obe','4MT1vDqEKurI3ctpK6TqLt','4nSgEvZncnC5oNPVrtwnLd','3gNRdx3DyEnckHDCmVwwnY','54P0u0BOmRdmtEVPgcoZy0','2AbQwU2cuEGfD465wCXlg2')
    # artists = ('7mUBMaZW1MXGswaneb0JTT','77aLk6J8ofnVxa1eXK9jiU','4PPoI9LuYeFX8V674Z1R6l','1NiC1V6xc8OR1ERiIoCvtx','2uyweLa0mvPZH6eRzDddeB','4mN0qcMxWX8oToqfDPM5yV','7FsRH5bw8iWpSbMX1G7xf1')
    # artists = ('6qhOH2mrlqUDod9sWA5kR2','2MRBDr0crHWE5JwPceFncq','4etuCZVdP8yiNPn4xf0ie5','796OSRuB0E9Hq55uTFL9U8','15YnmlNukYCFvwaFnoDwwV','2nrSPPSfNesng85eRV4W4m','72v53CufRiSyqcQ78KUQ5p')
    # artists = ('0XwVARXT135rw8lyw1EeWP','1SykQGBiBwkQ1fcGpJ1BJt','0D5U7oXEE4dut2DPyUDLca','5R6YR0pasdxlynyq0Abq7x','2osoVujXgV0PA8lhqDKYFw','2gDqGAadPIPiA7LtmNn74g','7x5Slu7yTE5icZjNsc3OzW')
    # artists = ('4wLXwxDeWQ8mtUIRPxGiD6','3VCrybIJKH7UurbDcZbMmn','73SBwOgH6mrS09OyFHdR62','3SCOuAxngTC1yGjKMcIPEd','5sIuOfUs74K1zFv5BqVaQY','4bsuyZ9PwHp2PsviqT1clB','4JtUybFExZ5dbq3GyYwRE5')
    # artists = ('0KdPDmQhHxBKsHNsQuh5ry','4i5rDrP2IqCdMgde0vIpyB','1Y2yzHPbBWZouNYTOGFq7u','07ORe1OIPJ0bjk4Fs9nQEK','6GoZ2axiSqX91WzMrvJfWk','0SJy1J0FgP21lbvGBMKT8H','7EXwl78TqHmZ78cV3sc37C')
    # artists = ('72R3RMGmSmzG57R7OUaDaN','3rs3EOlJ8jyPpdGiQ9Mhub','4tLUnrSgMM7tT0zVs3wX61','1LKPL2O3vA3ozNsmshDg3o','4vQV1LCGBdYAt5rIIPjSFZ','1c84wItoiAe1pEbpJMqUmQ','6nnspeopmJAG07xOxHmqTu')
    # artists = ('7opp16lU7VM3l2WBdGMYHP','5BwMgvRwlq61SmknvsVIQj','5c4wQaXkNDqSOTjqX4ExAu','01rgao9OzfBm2BOHWJpi1Y','70OAdYggwWl6EApsgp1jNX','6VGjtnnXEadiBtE5xPStM2','7umWQMinvyqkJIWOdo02OW')
    # artists = ('3CoaObestry7i9joSvJ2hK','41EMdaUylPIcdbGdojyr2O','1FlYevYLENR3IMgMlnMvf9','0G2qO3Wbj6WmCTFgcsJ1Eo','13or1Wf6ipcvSIiurZATvw','1r4hJ1h58CWwUQe3MxPuau','1vyhD5VmyZ7KMfW5gqLgo5')
    # artists = ('4VMYDCV2IEDYJArk749S6m','1wZtkThiXbVNtj6hee6dz9','0eHQ9o50hj6ZDNBt6Ys1sD','4q3ewBCX7sLwd24euuV69X','21451j1KhjAiaYKflxBjr1','4SsVbpTthjScTS7U2hmr1X','790FomKkXshlbRYZFtlgla')
    # artists = ('0tmwSHipWxN12fsoLcFU3B','2R21vXR83lH98kGeO99Y66','1ykothWH0xl8drRyJWuw7I','3vQ0GE3mI0dAaxIMYe5g7z','5DUlefCLzVRzNWaNURTFpK','1i8SpTcr7yvPOmcqrbnVXY','2OHKEe204spO7G7NcbeO2o')
    # artists = ('1mcTU81TzQhprhouKaTkpq','7iK8PXO48WeuP03g8YR51W','1SupJlEpv7RS2tPNRaHViT','00me4Ke1LsvMxt5kydlMyU','329e4yvIujISKGKz1BZZbO','4IMAo2UQchVFyPH24PAjUs','33ScadVnbm2X8kkUqOkC6Z')
    # artists = ('6XFITTl7cFTdopDY3lUdlY','4bw2Am3p9ji3mYsXNXtQcd','0n7Nj264FyQMi1YZpMN1vY','47MpMsUfWtgyIIBEFOr4FE','07YUOmWljBTXwIseAUd9TW','2wkoKEfS6dXwThbyTnZWFU','28gNT5KBp7IjEOQoevXf9N')
    # artists = ('2OnKRchqP7tT0FzTvWIFI7','3EiLUeyEcA6fbRPSHkG5kb','5lFhCi03HDneWzvCxGctrT','7tU1VKOuxiNZwBZC6RHidA','4QVBYiagIaa6ZGSPMbybpy','2SIZkgqao1WVQAuliN0PN4','39yVoqm6sYFvvqF1RciUVf')
    # artists = ('5vLOlJcOKe9DfBC5LeLpSs','2wMN1UAgISJA8yQusQL18G','72VywtXEoONiBLNu3ibGI7','2iEDalkx4bi0VkRuW0QkYD','5byIHYV7DDUKtHPAMyf3lA','0OluGbRuQQEcYyttGww517','7GkhznErka8OWEHJS05Dpd')
    # artists = ('2Mk7yrY8Dt93tvVhyxh8Zj','3vKxuOGRkXJWpCZPf01Nj8','2a15NvJ0ASGPEuWgGCCIJC','1LMyTeRhjaitILs98h3MaF','6c0qylj1D1gqcUUN2P8Ofp','0zgFL90nGTrH2iOMD8Vysy','5kt4v3JNtP8svtTI8PDFOT')
    # artists = ('1v7iZcyrm4fHfsEBiseomy','4kcnsS1aAB40FMcLD01gmI','3E6xrwgnVfYCrCs0ePERDz','2LRoIwlKmHjgvigdNGBHNo','2e4nwiX8ZCU09LGLOpeqTH','5mudirGeAjQgkS2AaIQVCb','7fAKtXSdNInWAIf0jVUz65')
    # artists = ('1qBGWp46vgiATN7mfKJd3s','4NEYQeEYBUjfaXgDQGvFvu','61J0BktHv7PuP3tjTPYXSX','6ZZ2DeepA3GpoGU4KwqSlU','1Pu2OFhNGOTakxDgxoIXiv','5M9Bb4adKAgrOFOhc05Y50','7M5Z4j6N9k2Jd3CukFUv5e')
    # artists = ('2L0nCuTUHFPHC3Y8uqbUKw','30xVFd5hiy33d6mrczbNzZ','36eqG3jM0MhxTR7Cuw7BQA','1OUDQLymoysITxprkd0Qvj','5fyAJtTzITeqGwxxtoYnaa','1Pe4MoTbike2NZeexUUBrU','0NJbkbtOgSj2Q5bkUV3FPz')
    # artists = ('77ziqFxp5gaInVrF2lj4ht','00XhexlJEXQstHimpZN910','7hIqJfRYGBWWT1Qxu6Cpd2','5bWUlnPx9OYKsLiUJrhCA1','14zUHaJZo1mnYtn6IBRaRP','2cPqdH7XMvwaBJEVjheH8g','5Rj6rNR8zIlUUDCs1OyPmW')
    # artists = ('1vrahybrKylgwkjhbmOz94','6LgCpm1Br63qTr0l9WagKQ','1MtgoOhWrRaiNm4d3y3W3W','3anoxp3DkA74doyHgkDngp','5SyvBTttsNPEcFjtceTBmx','76wScr6deBbR8quNo1UxJI','4JRKcLbpjobmoOVoOXPd6y')
    # artists = ('1Lvrnoz3ZKzzrBuZ446e6P','3K8X4ZoPqijzc6QSP4eAQF','2ae7hwWgesyGJVI2vebofH','6npvMAuRzmnkSxIlxwdG0T','0UTzLuwz9RvFOCnwAZjUxn','6AvVNBiwAW7CXZPACAo2OB','4gtaTXIhBK1iyVUAkB2YZu')
    # artists = ('1sEGUJyocmOnW6emzgoHMM','4Srl3qf5e1RfnXi5wBlIL4','2sSqkk6j5gRa7MzeQqMfIN','4a3ZMZGCMmCEAFnRdUTdw4','3IZxs4ZukiitIk8vkAPAxC','5PoJhiT21fXvZitg3guhiJ','2vylKAxeoJ2dAwIi9ck762')
    # artists = ('63AURDJ3zaxKaBcrm9q74B','5zaG384VZzAb6AMfEnSy2r','1GDbiv3spRmZ1XdM1jQbT7','6ELAHXutcbgmM3v0Bg2nei','4bCJFFuTF8fuditJEIS1GX','5388C04OP0Fc6xqbvct7kv','23cijmutocNvhM5xkcyyFF')
    # artists = ('3QyEoyQFrPTPxE01tTxjNm','3YbOSxo85kla7RID8ugnW3','7ltDVBr6mKbRvohxheJ9h1','5GcWBUX00IPuWVGMIRK1sS','1CztIa6fCQ0WmVPidXuwSs','66q4aUeE6L8715QQ2yD68G','1dbp04JzZ81JXlMGupCnJ8')
    # artists = ('5x3mrCTZmkoTXURN7pWdGN','0eecdvMrqBftK0M1VKhaF4','40KS6MHytlDIWwQQwbfETj','0G7A5LzQAs2egiQl7hO5tV','4cK5uxWRVJ3QOSfaBMX2Ex','5aINmhPWfAHvZ5qaMdBezq','6VCoG3MG7ZKRxDjaYOvtrF')
    # artists = ('6nxwdNlg4g7FrLZZB43n5v','2Bo0gW1bqWSjD27xOcVtjg','58pqy50vIEhqbk6ad978VJ','7aTwbcPoqJOzeEh96WHxrp','4qKJA8Cf8R44cMThP6q8KM')

    for artist_id in artists:
        artist_object = collector.getArtistObject(artist_id)
        collector.getArtistAlbums(artist_object)
    return render(request, 'collector/search_artist.html', {'message': 'ok'})
