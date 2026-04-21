BASE64_ENCODING = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"


def encode_in_base64(counter) -> str:
    digits = []
    while counter > 0:
        quotient = counter // 64
        rem = counter % 64
        digits.append(rem)
        counter = quotient
    digits.reverse()
    encoding = "".join([BASE64_ENCODING[digit] for digit in digits])
    return encoding


class Codec:
    def __init__(self):
        self.mappings = dict()
        self.counter = 1
        self.prefix = "https://leetcode.com/problems/"

    def encode(self, longUrl: str) -> str:
        """Encodes a URL to a shortened URL."""
        shortUrl = self.prefix + encode_in_base64(self.counter)
        # print(f"Created short-url {shortUrl} for passed long-url {longUrl}")
        self.counter = self.counter + 100
        self.mappings[shortUrl] = longUrl
        return shortUrl

    def decode(self, shortUrl: str) -> str:
        """Decodes a shortened URL to its original URL."""
        return self.mappings[shortUrl]


if __name__ == "__main__":
    # Your Codec object will be instantiated and called as such:
    codec = Codec()
    for url in [
        "url1",
        "url2",
        "url3",
        "url4",
        "url5",
        "url6",
        "url7",
        "url8",
        "url9",
        "url10",
        "url11",
        "url12",
        "url13",
        "url14",
        "url15",
        "url16",
    ]:
        shortUrl = codec.encode(url)
        decodedLongUrl = codec.decode(shortUrl)
        if decodedLongUrl != url:
            print(
                f"Error: decoding didn't work correctly for url {url}. "
                f"Got decoded URL: {decodedLongUrl}"
            )
