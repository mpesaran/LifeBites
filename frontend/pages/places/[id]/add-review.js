import { useRouter } from 'next/router';
import { useState } from 'react';
import { Box, Textarea, Button, Heading } from '@chakra-ui/react';
import axios from 'axios';
import {FormControl, FormLabel} from "@chakra-ui/form-control";
import { toast } from 'react-toastify';


export default function AddReviewPage() {
    const router = useRouter();
    const { id } = router.query; // Access the place ID from the URL
    const [reviewData, setReviewData] = useState({ text: '', rating: 1 });
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);

    const handleInputChange = (e) => {
        setReviewData({ ...reviewData, [e.target.name]: e.target.value });
    };

    const handleReviewSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
        const response = await axios.post(
            `http://127.0.0.1:5000/api/v1/reviews/`,
            {
            text: reviewData.text,
            rating: reviewData.rating,
            place_id: id, 
            user_id: '6ad904d1-f9c3-40a7-9b48-f14d306813d4', // Hardcoded user ID
            }
        );

        toast.success('Review submitted successfully!', {
            position: "top-right",
            autoClose: 3000,
        });

        setTimeout(() => {
            router.push(`/places/${id}`); 
        }, 3000);

        } catch (error) {
        console.error('Error submitting review:', error);

        toast.error('Failed to submit review.', {
            position: "top-right",
            autoClose: 3000,
        });

        } finally {
        setLoading(false);
        }
    };

    return (
        <Box>
        <Box maxW="xl" mx="auto" py={8}>
            <Heading as="h2" size="lg" mb={6}>Add a Review</Heading>

            {message && <Box mb={4}>{message}</Box>}

            <Box as="form" onSubmit={handleReviewSubmit}>
            <FormControl isRequired>
                <FormLabel>Review Text</FormLabel>
                <Textarea
                value={reviewData.text}
                onChange={(e) => setReviewData({ ...reviewData, text: e.target.value })}
                mb={4}
                />
            </FormControl>

            <FormControl isRequired>
                <FormLabel>Rating (1-5)</FormLabel>
                <Textarea
                type="number"
                min={1}
                max={5}
                value={reviewData.rating}
                onChange={(e) => setReviewData({ ...reviewData, rating: e.target.value })}
                mb={4}
                />
            </FormControl>

            <Button type="submit" colorScheme="teal" isLoading={loading}>
                Submit Review
            </Button>
            </Box>
        </Box>
        </Box>
    );
    }
