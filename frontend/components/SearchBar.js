import { Input, InputGroup, InputLeftElement } from "@chakra-ui/react"
import { FaSearch } from "react-icons/fa"


export default function SearchBar({ value, onChange }) {
  return (
    <InputGroup mb={6}>
      {/* <InputLeftElement pointerEvents="none">
        <FaSearch color="gray.300" />
      </InputLeftElement> */}
      <Input
        type="text"
        placeholder="Search places..."
        value={value}
        onChange={onChange}
        bg="white"
        shadow="sm"
      />
    </InputGroup>
  )
}
