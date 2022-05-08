# The Project

---

The project was designed to build an API that allows fast searches for [anagrams](https://en.wikipedia.org/wiki/Anagram). 
`dictionary.txt` is a text file containing every word in the English dictionary. 

The API responds on the following endpoints as specified.

- `POST /words.json`: Takes a JSON array of English-language words and adds them to the corpus (data store).
- `POST /anagrams`: Takes a set of words and returns whether these words are all anagrams of each other.
- `GET /anagrams/{word}.json`:
  - Returns a JSON array of English-language words that are anagrams of the word passed in the URL.
  - This endpoint supports an optional query param that indicates the maximum number of results to return.
  - This endpoint also supports an additional query param that indicates whether to include proper nouns in 
 the list of anagrams
- `GET /dictionary/stats`: Returns a count of words in the corpus and min, max, median, and average word length
- `GET /anagrams`:  
  - Returns the words with the most anagrams.
  - This endpoint supports an optional parameter `size`. When passed, it returns words with anagrams of passed size.
  - This endpoint also supports an additional query params that indicates whether to include proper nouns in the and 
  the maximum number of results to return, the default limit is 5. 
  list of anagrams and that indicates the maximum number of results to return
- `DELETE /words/{word}.json`: Deletes a single word from the data store.
- `DELETE /words.json`: Deletes all contents of the data store.
- `DELETE /anagrams/{word}.json`: Deletes a word and all of its anagrams

## Usage
Assuming the API is being served on localhost port 8000
  - For additional documentation on the apis check - `http://127.0.0.1:8000/docs`

```{bash}
# Adding words to the corpus
$ curl -i -X POST -d '{ "words": ["read", "dear", "dare"] }' http://localhost:8000/words.json
HTTP/1.1 201 Created
...

```{bash}
# ceck if certain words are anagrams
$ curl -i -X POST -d '{ "words": ["read", "dear", "dare"] }' http://localhost:8000/anagrams
HTTP/1.1 200 OK
...
true

# Fetching anagrams
$ curl -i http://localhost:8000/anagrams/read.json
HTTP/1.1 200 OK
...
{
  anagrams: [
    "ared",
    "daer",
    "dare",
    "dear"
  ]
}

# Specifying maximum number of anagrams
$ curl -i http://localhost:8000/anagrams/read.json?limit=1
HTTP/1.1 200 OK
...
{
  anagrams: [
    "ared"
  ]
}

# Fetching words with the anagrams of size 5
$ curl -i http://localhost:8000/anagrams?size=5&limit=1
HTTP/1.1 200 OK
...
[
  {"anagrams":
    ["Astilbe","astilbe","bestial","blastie","stabile"]
  }
]

# Delete single word
$ curl -i -X DELETE http://localhost:8000/words/read.json
HTTP/1.1 204 No Content
...

# Delete word with anagrams
$ curl -i -X DELETE http://localhost:8000/anagrams/read.json
HTTP/1.1 204 No Content
...


# Delete all words
$ curl -i -X DELETE http://localhost:8000/words.json
HTTP/1.1 204 No Content
...
```

## Implementation details
This project was written in Python3 using FastApi framework. The data is stored in PostgresDB.

## Additional Features
Some additional features I think can be implemented in the program.
- Check if a word exists in the dictionary.
- Get anagrams for phrases and sentences.
- Get words with most anagrams by length of words.

Note that a word is not considered to be its own anagram.

