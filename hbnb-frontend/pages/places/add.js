import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { Input, Button, Textarea, Box , } from '@chakra-ui/react';
import { FormControl, FormLabel, CheckboxGroup, Checkbox} from "@chakra-ui/form-control"
import { toast } from 'react-toastify';
import axios from 'axios';

export default function CreatePlacePage() {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: '',
    latitude: '',
    longitude: '',
    owner_id: '089c8a22-cd98-4654-bccc-6420874ffd87',
  });
  const [amenities, setAmenities] = useState([]);
  const [selectedAmenities, setSelectedAmenities] = useState([]);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  useEffect(() => {
    async function fetchAmenities() {
      const res = await axios.get('http://127.0.0.1:5000/api/v1/amenities/');
      setAmenities(res.data);
    }
    fetchAmenities();
  }, []);

  const handleAmenitiesChange = (selected) => {
    setSelectedAmenities(selected);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const dataToSend = {
        title: formData.title,
        description: formData.description,
        price: parseFloat(formData.price),
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        owner_id: formData.owner_id,
    };

    try {
        const response = await axios.post('http://127.0.0.1:5000/api/v1/places/', dataToSend, {
            headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
        throw new Error('Failed to create place');
    }

    const result = await response.json();
    toast({
        title: 'Place created.',
        description: `New place "${result.title}" has been added successfully.`,
        status: 'success',
        duration: 2000,
        isClosable: true,
    });

    router.push(`/places/${result.id}`);
    } catch (error) {
      toast({
        title: 'Error.',
        description: error.message,
        status: 'error',
        duration: 2000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box maxW="md" mx="auto" mt="8" p="4" borderWidth={1} borderRadius="md">
      <form onSubmit={handleSubmit}>
        <FormControl mb="4">
          <FormLabel htmlFor="title">Title</FormLabel>
          <Input
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </FormControl>

        <FormControl mb="4">
          <FormLabel htmlFor="description">Description</FormLabel>
          <Textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
          />
        </FormControl>

        <FormControl mb="4">
          <FormLabel htmlFor="price">Price</FormLabel>
          <Input
            type="number"
            id="price"
            name="price"
            value={formData.price}
            onChange={handleChange}
            required
          />
        </FormControl>

        <FormControl mb="4">
          <FormLabel htmlFor="latitude">Latitude</FormLabel>
          <Input
            type="number"
            id="latitude"
            name="latitude"
            value={formData.latitude}
            onChange={handleChange}
            required
          />
        </FormControl>

        <FormControl mb="4">
          <FormLabel htmlFor="longitude">Longitude</FormLabel>
          <Input
            type="number"
            id="longitude"
            name="longitude"
            value={formData.longitude}
            onChange={handleChange}
            required
          />
        </FormControl>

        <FormControl mb="4">
          <FormLabel>Amenities</FormLabel>
          {/* <CheckboxGroup value={selectedAmenities} onChange={handleAmenitiesChange}>
            {amenities.map((amenity) => (
              <Checkbox key={amenity.id} value={amenity.id}>
                {amenity.name}
              </Checkbox>
            ))}
          </CheckboxGroup> */}
        </FormControl>

        <Button
          mt="4"
          colorScheme="teal"
          type="submit"
          isLoading={loading}
          loadingText="Creating..."
        >
          Create Place
        </Button>
      </form>
    </Box>
  );
}
