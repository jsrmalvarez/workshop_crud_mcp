import React, { useState, useEffect } from 'react';
import { Box, Container, Heading, useToast } from '@chakra-ui/react';
import ItemsList from './components/ItemsList';
import ItemForm from './components/ItemForm';
import axios from 'axios';

function App() {
  const [items, setItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const toast = useToast();

  // Fetch items from API
  const fetchItems = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/api/items/');
      setItems(response.data);
    } catch (error) {
      console.error('Error fetching items:', error);
      toast({
        title: 'Error fetching items',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Submit batch of items
  const submitBatch = async (batchItems) => {
    try {
      const response = await axios.post('http://localhost:8000/api/items/batch', {
        items: batchItems
      });
      
      // Add successful items to the list
      if (response.data.success && response.data.success.length > 0) {
        setItems([...items, ...response.data.success]);
      }

      // Show warnings for failed items
      if (response.data.failed && response.data.failed.length > 0) {
        response.data.failed.forEach(failure => {
          toast({
            title: 'Item creation failed',
            description: `Failed to create item "${failure.item.title}": ${failure.error}`,
            status: 'warning',
            duration: 5000,
            isClosable: true,
          });
        });
      }

      return response.data;
    } catch (error) {
      console.error('Error submitting batch:', error);
      throw error;
    }
  };

  // Delete item
  const deleteItem = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/api/items/${id}`);
      setItems(items.filter(item => item.id !== id));
      return true;
    } catch (error) {
      console.error('Error deleting item:', error);
      throw error;
    }
  };

  // Update item
  const updateItem = async (id, updatedItem) => {
    try {
      const response = await axios.put(`http://localhost:8000/api/items/${id}`, updatedItem);
      setItems(items.map(item => item.id === id ? response.data : item));
      toast({
        title: 'Item updated',
        description: `${response.data.title} has been successfully updated`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      return response.data;
    } catch (error) {
      console.error('Error updating item:', error);
      throw error;
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  return (
    <Container maxW="container.xl" py={8}>
      <Heading as="h1" mb={6} textAlign="center">CRUD Application</Heading>
      <Box mb={10}>
        <ItemForm onSubmitBatch={submitBatch} />
      </Box>
      <ItemsList 
        items={items} 
        isLoading={isLoading} 
        onDeleteItem={deleteItem}
        onUpdateItem={updateItem}
      />
    </Container>
  );
}

export default App;