Shizoid.da, [10.04.21 03:59]
#include <iostream>
#include <time.h>
#include <math.h>
#include <unordered_map>
#define loadFactor 5.5

using namespace std;

struct plane
{
    char company;
    int weight;
    int maxSpeed;
    plane()
    {
        company = (int)(rand()%26 + 97);
        weight = rand()%9000 + 1;
        maxSpeed = rand()%330 + 70;
    }
};

long long generateRandLong()
{
    long long key = 0;
    for(int i=9; i>=0; i--)
    {
        if(i==9)
        {
            key+=pow(10, i)*(rand()%9 + 1);
        }
        else
        {
            key+=pow(10, i)*(rand()%10);
        }
    }
    return key;
}

struct HashNode
{
    long long key;
    plane newPlane;
    HashNode* nextHNode = NULL;
};


struct LinkedList
{
    HashNode* head = NULL;
    void push_front(long long key, plane newPlane)
    {
        HashNode* newHNode = new HashNode();
        newHNode->newPlane = newPlane;
        newHNode->key = key;
        newHNode->nextHNode = NULL;
        if(head == NULL)
        {
            head = newHNode;
        }
        else
        {
            newHNode->nextHNode = head;
            head = newHNode;
        }
    }

    bool pop_element(long long neededKey)
    {
        if (head == NULL) return false;
        if(head->key == neededKey)
        {
            HashNode* tmp = head;
            head = head->nextHNode;
            delete tmp;
            return true;
        }
        HashNode* currHNode = head;
        while(currHNode->nextHNode != NULL && currHNode->nextHNode->key != neededKey)
        {
            currHNode = currHNode->nextHNode;
        }
        if (currHNode->nextHNode == NULL) return false;
        HashNode* tmp = currHNode->nextHNode;
        currHNode->nextHNode = currHNode->nextHNode->nextHNode;
        delete tmp;
        return true;
    }

    ~LinkedList()
    {
        HashNode* currHNode = head;
        while(currHNode != NULL)
        {
            HashNode* tmpNode = currHNode;
            currHNode = currHNode->nextHNode;
            delete tmpNode;
        }
    }
};

struct HashTable
{
    int M = 8;
    LinkedList* bucketsArray = new LinkedList[M];
    int counter = 0;
    int alpha = 2;
    int hashfunc(long long key) //multiplication method
    {
        float A = (sqrt(5)-1)/2;
        return (M*(fmod(key * A, 1)));
    }

    plane* find(long long key)
    {
        int index = hashfunc(key);
        HashNode* currHNode = bucketsArray[index].head;
        //cout << currHNode << endl;
        while(currHNode != NULL)
        {
            if(currHNode->key == key)
            {
                return &currHNode->newPlane;
            }
            else
            {
                currHNode = currHNode->nextHNode;
            }
        }
        return NULL;
    }

    void insert(long long key, plane newPlane)
    {
        if(find(key) != NULL)
        {
            *find(key) = newPlane;
        }
        else
        {
            if((float)(size())/M >= loadFactor)
            {
                int pastSize = M;
                M*=alpha;
                LinkedList* newBucketsArray = new LinkedList[M];
                for(int i = 0; i<pastSize; i++)
                {
                    for(HashNode* currHNode = bucketsArray[i].head; currHNode != NULL; currHNode=currHNode->nextHNode)
                    {
                        newBucketsArray[hashfunc(currHNode->key)].push_front(currHNode->key, currHNode->newPlane);
                    }
                }
                delete[] bucketsArray;
                bucketsArray = newBucketsArray;
            }
            bucketsArray[hashfunc(key)].push_front(key, newPlane);
            counter++;
        }
    }

    void erase(long long key)
    {

        if(bucketsArray[hashfunc(key)].pop_element(key))
        {
            counter--;
        }
    }

    int size()
    {
        return counter;
    }

};

bool testHashTable()
{
    const int iters = 10000;     const int keysAmount = iters * 1;

Shizoid.da, [10.04.21 03:59]
// generate random keys:
    long long* keys = new long long[keysAmount];
     long long* keysToInsert = new long long[iters];
       long long* keysToErase = new long long[iters];
        long long* keysToFind = new long long[iters];
     for (int i = 0; i < keysAmount; i++)
    {
        keys[i] = generateRandLong();
    }
    for (int i = 0; i < iters; i++)
    {
        keysToInsert[i] = keys[generateRandLong() % keysAmount];         keysToErase[i] = keys[generateRandLong() % keysAmount];         keysToFind[i] = keys[generateRandLong() % keysAmount];
    }

    // test my HashTable:
    HashTable hashTable;
     clock_t myStart = clock();     for (int i = 0; i < iters; i++)
    {
        hashTable.insert(keysToInsert[i], plane());     }
    int myInsertSize = hashTable.size();     for (int i = 0; i < iters; i++)
    {
        hashTable.erase(keysToErase[i]);
    }
    int myEraseSize = hashTable.size();     int myFoundAmount = 0;     for (int i = 0; i < iters; i++)
    {
        if (hashTable.find(keysToFind[i]) != NULL)
        {
            myFoundAmount++;
        }     }
    clock_t myEnd = clock();
    float myTime = (float(myEnd - myStart)) / CLOCKS_PER_SEC;

    // test STL hash table:
    unordered_map<long long, plane> unorderedMap;
     clock_t stlStart = clock();     for (int i = 0; i < iters; i++)
    {
        unorderedMap.insert({keysToInsert[i], plane()});
    }
    int stlInsertSize = unorderedMap.size();     for (int i = 0; i < iters; i++)
    {
        unorderedMap.erase(keysToErase[i]);
    }
    int stlEraseSize = unorderedMap.size();     int stlFoundAmount = 0;     for (int i = 0; i < iters; i++)
    {
        if (unorderedMap.find(keysToFind[i]) != unorderedMap.end())
        {
            stlFoundAmount++;
        }     }
    clock_t stlEnd = clock();
    float stlTime = (float(stlEnd - stlStart)) / CLOCKS_PER_SEC;

    cout << "My HashTable:" << endl;     cout << "Time: " << myTime << ", size: " << myInsertSize << " - " << myEraseSize << ", found amount: " << myFoundAmount << endl;     cout << "STL unordered_map:" << endl;     cout << "Time: " << stlTime << ", size: " << stlInsertSize << " - " << stlEraseSize << ", found amount: " << stlFoundAmount << endl << endl;

    delete keys;     delete keysToInsert;     delete keysToErase;     delete keysToFind;

    if (myInsertSize == stlInsertSize && myEraseSize == stlEraseSize && myFoundAmount == stlFoundAmount)
    {
        cout << "The lab is completed" << endl;         return true;
    }
    cerr << ":(" << endl;     return false;
}


int main()
{
    srand(time(NULL));
    testHashTable();
    return 0;
}