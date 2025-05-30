import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Textarea,
  Switch,
  FormErrorMessage,
  Heading,
  HStack,
  useToast,
  VStack
} from '@chakra-ui/react';
import { AddIcon } from '@chakra-ui/icons';

const ItemForm = ({ onAddItem, onSubmitBatch }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    is_active: true
  });
  const [tempItems, setTempItems] = useState([]);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const toast = useToast();

  const validateForm = () => {
    const newErrors = {};
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleAddToList = (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    // Add to temporary list
    setTempItems([...tempItems, { ...formData }]);
    toast({
      title: 'Item added to batch',
      description: `${formData.title} has been added to the batch`,
      status: 'success',
      duration: 2000,
      isClosable: true,
    });
    
    // Reset form
    setFormData({
      title: '',
      description: '',
      is_active: true
    });
  };

  const handleSubmitBatch = async () => {
    if (tempItems.length === 0) {
      toast({
        title: 'No items to submit',
        description: 'Please add at least one item to the batch',
        status: 'warning',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmitBatch(tempItems);
      setTempItems([]); // Clear temporary items after successful submission
      toast({
        title: 'Batch submitted',
        description: `Successfully submitted ${tempItems.length} items`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      console.error('Error submitting batch:', error);
      toast({
        title: 'Error submitting batch',
        description: error.response?.data?.detail || error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Box p={5} shadow="md" borderWidth="1px" borderRadius="md">
      <Heading size="md" mb={4}>Add New Items (Batch)</Heading>
      <form onSubmit={handleAddToList}>
        <FormControl isRequired isInvalid={!!errors.title} mb={4}>
          <FormLabel>Title</FormLabel>
          <Input
            name="title"
            value={formData.title}
            onChange={handleInputChange}
            placeholder="Enter item title"
          />
          {errors.title && <FormErrorMessage>{errors.title}</FormErrorMessage>}
        </FormControl>

        <FormControl mb={4}>
          <FormLabel>Description</FormLabel>
          <Textarea
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            placeholder="Enter item description (optional)"
            resize="vertical"
          />
        </FormControl>

        <FormControl display="flex" alignItems="center" mb={4}>
          <FormLabel htmlFor="is-active" mb="0">
            Active
          </FormLabel>
          <Switch
            id="is-active"
            name="is_active"
            isChecked={formData.is_active}
            onChange={handleInputChange}
          />
        </FormControl>

        <HStack spacing={4}>
          <Button
            type="submit"
            colorScheme="blue"
            leftIcon={<AddIcon />}
          >
            Add to Batch
          </Button>
          <Button
            colorScheme="green"
            onClick={handleSubmitBatch}
            isLoading={isSubmitting}
            loadingText="Submitting"
            isDisabled={tempItems.length === 0}
          >
            Submit Batch ({tempItems.length} items)
          </Button>
        </HStack>
      </form>

      {tempItems.length > 0 && (
        <Box mt={6}>
          <Heading size="sm" mb={2}>Items in Batch:</Heading>
          <VStack align="stretch" spacing={2}>
            {tempItems.map((item, index) => (
              <Box 
                key={index} 
                p={2} 
                borderWidth="1px" 
                borderRadius="md"
                bg="gray.50"
              >
                <strong>{item.title}</strong> - {item.description || 'No description'} 
                ({item.is_active ? 'Active' : 'Inactive'})
              </Box>
            ))}
          </VStack>
        </Box>
      )}
    </Box>
  );
};

export default ItemForm;