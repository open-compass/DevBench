#ifndef QUEUE_H
#define QUEUE_H

#include <stdexcept>

template <class T>
class Queue{
    struct Node{
        Node *next= nullptr;
        T data;
    };
    Node* _rear= nullptr;
    Node* _front= nullptr;
public:
    virtual ~Queue(){
        while(_front != nullptr)pop();
    }
    bool empty(){
        /**
 * Checks if the data structure (such as a queue) is empty.
 *
 * This function determines whether the data structure is empty by checking if the
 * '_front' pointer (or equivalent) points to 'nullptr'. If '_front' is 'nullptr',
 * it indicates that there are no elements in the structure.
 *
 * Returns:
 *    bool: Returns 'true' if the data structure is empty (i.e., '_front' is 'nullptr'),
 *    and 'false' otherwise.
 */
        return _front == nullptr;
    }
    void push(const T& data){
        /**
* Adds a new element to the data structure.
*
* This function inserts a new element into the data structure. The element to be added
* is passed as a constant reference, indicating that the function will not modify the
* element being added. Depending on the nature of the data structure (e.g., stack, queue),
* this function may add the element to the end, the beginning, or some other position in
* the structure.
*
* Args:
*    data (const T&): The data to be added to the data structure. 'T' represents the type
*    of elements stored in the data structure.
*
* Returns:
*    void: This function does not return a value.
*/
        Node* newNode = new Node;
        if(_rear == nullptr){
            newNode->data=data;
            _rear= _front=newNode;
            return;
        }
        newNode->data=data;
        _rear->next=newNode;
        _rear=newNode;
    }
    T front(){
        /**
        * Retrieves the front element of the data structure (such as a queue).
        *
        * This function returns the element at the front of the data structure. If the data
        * structure is empty (indicated by '_front' being 'nullptr'), it throws an
        * std::out_of_range exception. This ensures that the function only returns a valid
        * element when the data structure is not empty.
        *
        * Returns:
        *    T: The front element of the data structure. The type 'T' represents the type of
        *    elements stored in the data structure.
        *
        * Throws:
        *    std::out_of_range: Thrown if the data structure is empty (i.e., '_front' is 'nullptr').
        */
        if(_front == nullptr)throw std::out_of_range("queue is empty");
        return _front->data;
    }
    T pop(){
        /**
 * Removes and returns the front element of the data structure (such as a queue).
 *
 * This function removes the element at the front of the data structure and returns it.
 * If the data structure is empty (indicated by '_front' being 'nullptr'), it throws an
 * std::out_of_range exception to indicate that there are no elements to pop. The function
 * also handles updating the pointers within the data structure to reflect the removal of
 * the front element.
 *
 * Returns:
 *    T: The data of the removed front element. The type 'T' represents the type of
 *    elements stored in the data structure.
 *
 * Throws:
 *    std::out_of_range: Thrown if the data structure is empty (i.e., '_front' is 'nullptr').
 */
        Node* willDequeue = _front;
        if(willDequeue== nullptr)throw std::out_of_range("queue is empty");
        _front = _front->next;
        T willReturn=willDequeue->data;
        if(willDequeue == _rear)_rear=nullptr;
        delete(willDequeue);
        return willReturn;
    }
};


#endif //QUEUE_H
