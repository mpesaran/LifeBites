import {
    Box, Button, Heading,
    Input, Stack, Text
  } from '@chakra-ui/react';
  import { useState } from 'react';
  import { useRouter } from 'next/router';
  import { toast } from 'react-toastify';
  import {FormControl, FormLabel} from "@chakra-ui/form-control"
  
  export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const router = useRouter();
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
  
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/users/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email,
            password,
          }),
        });
  
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Login failed.');
        }
  
        const data = await response.json();
  
        localStorage.setItem('user', JSON.stringify(data));
  
        toast({
          title: `Welcome, ${data.first_name}!`,
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
  
        router.push('/'); 
      } catch (err) {
        toast({
          title: err.message,
          status: 'error',
          duration: 3000,
          isClosable: true,
        });
      } finally {
        setLoading(false);
      }
    };
  
    return (
      <Box maxW="400px" mx="auto" p={6}>
        <Heading mb={6}>Login</Heading>
        <Stack as="form" spacing={4} onSubmit={handleSubmit}>
          <FormControl isRequired>
            <FormLabel>Email</FormLabel>
            <Input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
            />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Password</FormLabel>
            <Input
              type='password'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
            />
          </FormControl>
  
          <Button type="submit" colorScheme="teal" isLoading={loading}>
            Log In
          </Button>
  
          <Text textAlign="center">
            Dont have an account? <a href="/signup" style={{ color: 'teal' }}>Sign Up</a>
          </Text>
        </Stack>
      </Box>
    );
  }
  