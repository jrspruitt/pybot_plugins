##Words API##
A collection of APIs dealing with words, dictionaries, rhymes, thesaurus, etc.

**Commands:**

* Syntax: _cmd &lt;word&gt; \[index\]_

    * Word to search.

    * Index of results, reported as Total: num

* _define_

    * Returns: Standard dictionary definition.

* _thes_

    * Returns: An alternate word.

* _urband_

    * Returns: Urban Dictionary definition.

* _rhyme_

    * Returns: RhymeBrain rhyming words.


**Requirements:**

* dictionaryapi.com API key for define and bigwords

* mashape.com API key for Urban Dictionary


**config.py Changes**

[wordsapi]

* dict_apikey=dictionaryapi.com Collegiate API key.
* thes_apikey=dictionaryapi.com Thesaurus API key.
* urband_apikey=mashape.com API key.
