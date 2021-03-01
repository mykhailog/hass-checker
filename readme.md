# Home Assistant Availability Checker
Simple script which ping Home Assistant instance and notify user when server goes down.

<img src="https://user-images.githubusercontent.com/1454659/109507736-b59ca080-7aa7-11eb-96ea-55a257ed1586.png" width="400">

## Installation
```bash
    git clone git@github.com:mykhailog/hass-checker.git
    pip3 install requests
```

## Usage Example

```bash
export PUSH_TOKEN=Fnp9JD4ToroCpUl_:kiumxB8I8kOyKguty4XQ21UkNG70FtprFkixnb3xIUTyWxSj490f...
export HASS_URL=https://hass.mykhailo.com/
hass_checker
```

## How to Get Push Token
1. Open Home Assistant mobile app
2. Open sidebar and click App Configuration
3. Click Notification
4. Copy PUSH ID

![image](https://user-images.githubusercontent.com/1454659/109507098-0c55aa80-7aa7-11eb-8f86-ce6baad176e5.png)

*Warning:*
*Don't share or publish PUSH_TOKEN anywhere.*

---

### MIT License

Copyright (c) 2021 Mykhailo
