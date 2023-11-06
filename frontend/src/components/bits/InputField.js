import React from "react";
import styled from "styled-components";

const InputField = ({
	inputType = "text",
	placeholder = "",
	dark = false,
	onChangeCallback = () => {},
}) => {
	return (
		<>
			<Input
				type={inputType}
				autoCorrect="off"
				autoComplete="off"
				placeholder={placeholder}
				onChange={onChangeCallback}
				style={{ background: dark ? "#777" : "#f2f2f2" }}
			/>
		</>
	);
};

const Input = styled.input`
	border: none;
	appearance: none;
	-webkit-appearance: none;
	-ms-appearance: none;
	-moz-appearance: none;
	background: #f2f2f2;
	padding: 12px;
	border-radius: 3px;
	width: 300px;
	outline: none;
	font-size: 17px;
	font-family: "Roboto", sans-serif;

	::placeholder {
		color: #222222;
		font-size: 17px;
		font-family: "Roboto", sans-serif;
	}
`;

export default InputField;
