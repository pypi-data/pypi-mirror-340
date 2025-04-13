## 1.29.4 - 2025-04-13
### Extractors
#### Additions
- [chevereto] support `imagepond.net` ([#7278](https://github.com/mikf/gallery-dl/issues/7278))
- [webtoons] add `artist` extractor ([#7274](https://github.com/mikf/gallery-dl/issues/7274))
#### Fixes
- [deviantart] fix `KeyError: 'has_subfolders'` ([#7272](https://github.com/mikf/gallery-dl/issues/7272) [#7337](https://github.com/mikf/gallery-dl/issues/7337))
- [discord] fix `parent` keyword inconsistency ([#7341](https://github.com/mikf/gallery-dl/issues/7341) [#7353](https://github.com/mikf/gallery-dl/issues/7353))
- [E621:pool] fix `AttributeError` ([#7265](https://github.com/mikf/gallery-dl/issues/7265) [#7344](https://github.com/mikf/gallery-dl/issues/7344))
- [everia] fix/improve image extraction ([#7270](https://github.com/mikf/gallery-dl/issues/7270))
- [gelbooru] fix video URLs ([#7345](https://github.com/mikf/gallery-dl/issues/7345))
- [hentai2read] fix `AttributeError` exception for chapters without artist ([#7355](https://github.com/mikf/gallery-dl/issues/7355))
- [issuu] fix extractors ([#7317](https://github.com/mikf/gallery-dl/issues/7317))
- [kemonoparty] fix file paths with backslashes ([#7321](https://github.com/mikf/gallery-dl/issues/7321))
- [readcomiconline] fix `issue` extractor ([#7269](https://github.com/mikf/gallery-dl/issues/7269) [#7330](https://github.com/mikf/gallery-dl/issues/7330))
- [rule34xyz] update to API v2 ([#7289](https://github.com/mikf/gallery-dl/issues/7289))
- [zerochan] fix `KeyError: 'author'` ([#7282](https://github.com/mikf/gallery-dl/issues/7282))
#### Improvements
- [instagram] use Chrome `User-Agent` by default ([#6379](https://github.com/mikf/gallery-dl/issues/6379))
- [pixiv] support `phixiv.net` URLs ([#7352](https://github.com/mikf/gallery-dl/issues/7352))
- [tumblr] support URLs without subdomain ([#7358](https://github.com/mikf/gallery-dl/issues/7358))
- [webtoons] download JPEG files in higher quality
- [webtoons] use a default 0.5-1.5s delay between requests ([#7329](https://github.com/mikf/gallery-dl/issues/7329))
- [zzup] support `w.zzup.com` URLs ([#7327](https://github.com/mikf/gallery-dl/issues/7327))
### Downloaders
- [ytdl] fix `KeyError: 'extractor'` exception when `ytdl` reports an error ([#7301](https://github.com/mikf/gallery-dl/issues/7301))
### Post Processors
- [metadata] add `metadata-path` option ([#6582](https://github.com/mikf/gallery-dl/issues/6582))
- [metadata] fix handling of empty directory paths ([#7296](https://github.com/mikf/gallery-dl/issues/7296))
- [ugoira] preserve `extension` when using `"mode": "archive"` ([#7304](https://github.com/mikf/gallery-dl/issues/7304))
### Miscellaneous
- [formatter] add `i` and `f` conversions ([#6582](https://github.com/mikf/gallery-dl/issues/6582))
