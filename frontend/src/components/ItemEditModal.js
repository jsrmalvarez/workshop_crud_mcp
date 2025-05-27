import React, { useState, useEffect } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  FormControl,
  FormLabel,
  Input,
  Textarea,
  Switch,
  FormErrorMessage,
  useToast
} from '@chakra-ui/react';

const ItemEditModal = ({ isOpen, onClose, item, onUpdate }) => {
  const [formData, setFormData] = useState({
    id: '',
    title: '',
    description: '',
    is_active: true
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const toast = useToast();

  useEffect(() => {
    if (item) {
      setFormData({
        id: item.id,
        title: item.title,
        description: item.description || '',
        is_active: item.is_active
      });
    }
  }, [item]);

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
      await onUpdate(formData);
    } catch (error) {
      console.error('Error updating item:', error);
      toast({
        title: 'Error updating item',
        description: error.message || 'An unexpected error occurred',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Edit Item</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <form id="edit-item-form" onSubmit={handleSubmit}>
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
              <FormLabel htmlFor="edit-is-active" mb="0">
                Active
              </FormLabel>
              <Switch
                id="edit-is-active"
                name="is_active"
                isChecked={formData.is_active}
                onChange={handleInputChange}
              />
            </FormControl>
          </form>
        </ModalBody>

        <ModalFooter>
          <Button 
            variant="ghost" 
            mr={3} 
            onClick={onClose}
          >
            Cancel
          </Button>
          <Button 
            form="edit-item-form"
            type="submit"
            colorScheme="blue"
            isLoading={isSubmitting}
            loadingText="Updating"
          >
            Update
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default ItemEditModal;