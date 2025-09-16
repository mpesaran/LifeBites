import { Box, Button, Heading, Input, Stack, Text } from '@chakra-ui/react';
import { useState } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'react-toastify';
import {FormControl, FormLabel} from "@chakra-ui/form-control"

  
export default function Signup() {
    const [formData, setFormData] = useState({
      first_name: '',
      last_name: '',
      email: '',
      password: '',
    });
    const [loading, setLoading] = useState(false);
    const router = useRouter();
  
    const handleChange = (e) => {
      const { name, value } = e.target;
      setFormData((prev) => ({ ...prev, [name]: value }));
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
  
      try {
        console.log(JSON.stringify(formData));
        const response = await fetch('http://127.0.0.1:5000/api/v1/users/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData),
        });

        const data = await response.json(); 

        if (!response.ok) {
          throw new Error(data.message || 'Failed to sign up.');
        }
  
        // Show success toast
        toast.success('Account created successfully!', {
          position: "top-right",
          autoClose: 3000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
        });
  
        
        setTimeout(() => router.push('/'), 1000); 
      } catch (err) {
        // Show error toast
        toast.error(`Error: ${err.message}`, {
          position: "top-right",
          autoClose: 3000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
        });
      } finally {
        setLoading(false);
      }
    };
  
    return (
      <Box maxW="400px" mx="auto" p={6}>
        <Heading mb={6}>Sign Up</Heading>
        <Stack as="form" spacing={4} onSubmit={handleSubmit}>
          <FormControl isRequired>
            <FormLabel>First Name</FormLabel>
            <Input name="first_name" onChange={handleChange} />
          </FormControl>
  
          <FormControl isRequired>
            <FormLabel>Last Name</FormLabel>
            <Input name="last_name" onChange={handleChange} />
          </FormControl>
  
          <FormControl isRequired>
            <FormLabel>Email</FormLabel>
            <Input name="email" type="email" onChange={handleChange} />
          </FormControl>
  
          <FormControl isRequired>
            <FormLabel>Password</FormLabel>
            <Input name="password" type="password" onChange={handleChange} />
          </FormControl>
  
          <Button type="submit" colorScheme="teal" isLoading={loading}>
            Sign Up
          </Button>
  
          <Text textAlign="center">
            Already have an account? <a href="/login" style={{ color: 'teal' }}>Login</a>
          </Text>
        </Stack>
      </Box>
    );
  }