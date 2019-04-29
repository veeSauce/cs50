// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

int hashtable_size = 0;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
       // create a linked-list for all words
       node *new_node = malloc (sizeof(node));

       if (new_node== NULL)

       {
           unload();
           return false;
       }

       strcpy(new_node -> word, word);

       int hashed = hash(word);

       if (hastable[hashed] == NULL)
       {
           hashtable[hashed] == new_node;
       }
       else
       {
       new_node -> next = hashtable[0];
       hashtable[0] = new_node;
       }

       hashtable_size++;

    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return hashtable_size;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int hash = hash(word);

    if (hashtable[hash] == NULL)
    {
        return false;
    }
    else if (hashtable[hash] != NULL)
    {
        node *cursor = hashtable[hash];

        while (cursor != NULL)
        {
            int i;
            i = strcasecmp(cursor->word, word);
            if( i == 0)
            {
                return true;
            }
            else
            {
                cursor = cursor -> next;
            }
        }
    }

    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *cursor = hashtable[0];

    if (cursor == NULL)
    {
        unload();
        return false;
    }

    while (cursor != NULL)
    {
        cursor = cursor -> next;
        free(temp);
    }
}
