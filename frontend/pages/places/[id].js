import {
    Box,
    Heading,
    Text,
    Stack,
    Image,
    SimpleGrid,
    Container,
    Flex,
    Button,
} from '@chakra-ui/react';
import { useRouter } from 'next/router';
import axios from 'axios';
import Navbar from '@/components/Navbar';
import { useState } from 'react';

export async function getServerSideProps(context) {

    const { id } = context.params;
  
    try {
      const res = await axios.get(`http://127.0.0.1:5000/api/v1/places/${id}`);
      return {
        props: {
          place: res.data,
        },
      };
    } catch (err) {
      return {
        props: {
          place: null,
        },
      };
    }
  }
  
export default function PlaceDetails({ place }) {

    const router = useRouter();
    if (!place) {
      return <p>Loading...</p>;
    }
    console.log(place.amenities)
    const handleAddReviewClick = () => {
        router.push(`/places/${place.id}/add-review`);
      };
    return (
        <Box>
      <Navbar />

      <Container maxW="6xl" py={10}>
        {/* Image Banner */}
        <Image
          src={place.image_url || "/images/default.jpg"}
          alt={place.title}
          borderRadius="xl"
          w="100%"
          h={{ base: "250px", md: "400px" }}
          objectFit="cover"
          mb={8}
        />

        {/* Title + Owner/Location */}
        <Flex justify="space-between" align="center" mb={8} flexWrap="wrap">
          <Heading size="lg">{place.title}</Heading>
          <Stack spacing={1} textAlign="right" mt={{ base: 4, md: 0 }}>
            {place.owner && (
              <>
                <Text fontWeight="medium">{place.owner.first_name} {place.owner.last_name}</Text>
                <Text fontSize="sm" color="gray.500">{place.owner.email}</Text>
              </>
            )}
            <Text fontSize="sm" color="gray.500">
              📍 ({place.latitude}, {place.longitude})
            </Text>
          </Stack>
        </Flex>

        {/* Description */}
        <Box mb={8}>
          <Heading as="h2" size="md" mb={2}>Description</Heading>
          <Text color="gray.700">{place.description}</Text>
        </Box>

        {/* Amenities */}
        <Box mb={8}>
          <Heading as="h2" size="md" mb={4}>Amenities</Heading>
          {Array.isArray(place.amenities) && place.amenities.length > 0 ? (
            <SimpleGrid columns={{ base: 2, md: 4 }} spacing={4}>
              {place.amenities.map((amenity, idx) => (
                <Box
                  key={idx}
                  borderWidth="1px"
                  borderRadius="lg"
                  p={3}
                  textAlign="center"
                  fontSize="sm"
                  fontWeight="medium"
                  bg="gray.50"
                >
                  {amenity}
                </Box>
              ))}
            </SimpleGrid>
          ) : (
            <Text color="gray.500">No amenities listed.</Text>
          )}
        </Box>
          
        {/* Reviews */}
        <Box>
            <Heading as="h2" size="md" mb={4}>Reviews</Heading>
            {Array.isArray(place.reviews) && place.reviews.length > 0 ? (
                <Stack spacing={4}>
                {place.reviews.map((review) => (
                    <Box
                    key={review.id}
                    borderWidth="1px"
                    borderRadius="lg"
                    p={4}
                    bg="gray.50"
                    >
                    <Flex justify="space-between" mb={2}>
                        <Text fontWeight="bold">
                        {review.user.first_name} {review.user.last_name}
                        </Text>
                        <Text color="yellow.500" fontWeight="medium">
                        ⭐ {review.rating}
                        </Text>
                    </Flex>
                    <Text color="gray.700">{review.text}</Text>
                    </Box>
                    ))}
                    </Stack>
                ) : (
                    <Text color="gray.500">No reviews yet.</Text>
                )}
            </Box>
        <Box mt={10}>
          <Button colorScheme="teal" onClick={handleAddReviewClick}>
            Add Review
          </Button>
        </Box>

      </Container>
    </Box>
      );
  }
  