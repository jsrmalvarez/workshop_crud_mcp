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
  Badge,
  Checkbox
} from '@chakra-ui/react';
import { DeleteIcon, EditIcon } from '@chakra-ui/icons';
import ItemEditModal from './ItemEditModal';

const ItemsList = ({ items, isLoading, onDeleteBatch, onUpdateItem }) => {
  const [editItem, setEditItem] = useState(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedItems, setSelectedItems] = useState([]);
  const [isDeleting, setIsDeleting] = useState(false);
  const toast = useToast();

  // Handle selection
  const handleSelectItem = (itemId) => {
    setSelectedItems(prev => 
      prev.includes(itemId) 
        ? prev.filter(id => id !== itemId)
        : [...prev, itemId]
    );
  };

  // Handle select all
  const handleSelectAll = () => {
    setSelectedItems(
      selectedItems.length === items.length 
        ? [] 
        : items.map(item => item.id)
    );
  };

  // Handle batch delete
  const handleBatchDelete = async () => {
    if (selectedItems.length === 0) {
      toast({
        title: 'No items selected',
        description: 'Please select items to delete',
        status: 'warning',
        duration: 2000,
        isClosable: true,
      });
      return;
    }

    setIsDeleting(true);
    try {
      await onDeleteBatch(selectedItems);
      setSelectedItems([]); // Clear selection after successful deletion
      toast({
        title: 'Items deleted',
        description: `Selected items have been deleted`,
        status: 'success',
        duration: 2000,
        isClosable: true,
      });
    } catch (error) {
      console.error('Error deleting items:', error);
      toast({
        title: 'Error deleting items',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsDeleting(false);
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
      <HStack justify="space-between" mb={4}>
        <Heading size="md">Items List</Heading>
        {selectedItems.length > 0 && (
          <Button
            colorScheme="red"
            leftIcon={<DeleteIcon />}
            onClick={handleBatchDelete}
            isLoading={isDeleting}
            loadingText="Deleting..."
            size="sm"
          >
            Delete Selected ({selectedItems.length})
          </Button>
        )}
      </HStack>
      
      <TableContainer>
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>
                <Checkbox
                  isChecked={items.length > 0 && selectedItems.length === items.length}
                  isIndeterminate={selectedItems.length > 0 && selectedItems.length < items.length}
                  onChange={handleSelectAll}
                />
              </Th>
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
                <Td>
                  <Checkbox
                    isChecked={selectedItems.includes(item.id)}
                    onChange={() => handleSelectItem(item.id)}
                  />
                </Td>
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
                  <Button 
                    size="sm" 
                    colorScheme="blue" 
                    leftIcon={<EditIcon />} 
                    onClick={() => handleEdit(item)}
                  >
                    Edit
                  </Button>
                </Td>
              </Tr>
            ))}
            {items.length === 0 && !isLoading && (
              <Tr>
                <Td colSpan="7" textAlign="center">No items found</Td>
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