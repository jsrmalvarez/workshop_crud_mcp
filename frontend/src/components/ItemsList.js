import React, { useState } from 'react';
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableContainer,
  Heading,
  Button,
  useToast,
  HStack,
  Badge
} from '@chakra-ui/react';
import { DeleteIcon, EditIcon } from '@chakra-ui/icons';
import ItemEditModal from './ItemEditModal';

const ItemsList = ({ items, isLoading, onDeleteItem, onUpdateItem }) => {
  const [editItem, setEditItem] = useState(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const toast = useToast();

  // Handle delete
  const handleDelete = async (id) => {
    try {
      await onDeleteItem(id);
      toast({
        title: 'Item deleted',
        description: "Item has been successfully deleted",
        status: 'success',
        duration: 2000,
        isClosable: true,
      });
    } catch (error) {
      console.error('Error deleting item:', error);
      toast({
        title: 'Error deleting item',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  // Handle edit click
  const handleEdit = (item) => {
    setEditItem(item);
    setIsEditModalOpen(true);
  };

  // Handle item update
  const handleItemUpdate = async (updatedItem) => {
    try {
      await onUpdateItem(updatedItem.id, updatedItem);
      setIsEditModalOpen(false);
    } catch (error) {
      console.error('Error updating item:', error);
      toast({
        title: 'Error updating item',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Box p={5} shadow="md" borderWidth="1px" borderRadius="md">
      <Heading size="md" mb={4}>Items List</Heading>
      
      <TableContainer>
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>ID</Th>
              <Th>Title</Th>
              <Th>Description</Th>
              <Th>Status</Th>
              <Th>Created At</Th>
              <Th>Actions</Th>
            </Tr>
          </Thead>
          <Tbody>
            {items.map((item) => (
              <Tr key={item.id}>
                <Td>{item.id}</Td>
                <Td>{item.title}</Td>
                <Td>{item.description || 'N/A'}</Td>
                <Td>
                  <Badge colorScheme={item.is_active ? 'green' : 'red'}>
                    {item.is_active ? 'Active' : 'Inactive'}
                  </Badge>
                </Td>
                <Td>
                  {new Date(item.created_at).toLocaleString()}
                </Td>
                <Td>
                  <HStack spacing={2}>
                    <Button 
                      size="sm" 
                      colorScheme="blue" 
                      leftIcon={<EditIcon />} 
                      onClick={() => handleEdit(item)}
                    >
                      Edit
                    </Button>
                    <Button 
                      size="sm" 
                      colorScheme="red" 
                      leftIcon={<DeleteIcon />} 
                      onClick={() => handleDelete(item.id)}
                    >
                      Delete
                    </Button>
                  </HStack>
                </Td>
              </Tr>
            ))}
            {items.length === 0 && !isLoading && (
              <Tr>
                <Td colSpan="6" textAlign="center">No items found</Td>
              </Tr>
            )}
          </Tbody>
        </Table>
      </TableContainer>

      <ItemEditModal 
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        item={editItem}
        onUpdate={handleItemUpdate}
      />
    </Box>
  );
};

export default ItemsList;