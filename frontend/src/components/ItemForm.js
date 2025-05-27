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
  useToast
} from '@chakra-ui/react';
import { AddIcon } from '@chakra-ui/icons';

const ItemForm = ({ onAddItem }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    is_active: true
  });
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    try {
      const response = await onAddItem(formData);
      toast({
        title: 'Item created',
        description: `${response.title} has been successfully added`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      
      // Reset form
      setFormData({
        title: '',
        description: '',
        is_active: true
      });
      
    } catch (error) {
      console.error('Error creating item:', error);
      toast({
        title: 'Error creating item',
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
      <Heading size="md" mb={4}>Add New Item</Heading>
      <form onSubmit={handleSubmit}>
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

        <Button
          type="submit"
          colorScheme="green"
          isLoading={isSubmitting}
          loadingText="Submitting"
          leftIcon={<AddIcon />}
        >
          Add Item
        </Button>
      </form>
    </Box>
  );
};

export default ItemForm;