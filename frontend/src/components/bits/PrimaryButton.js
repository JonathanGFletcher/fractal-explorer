import React from "react";
import styled from "styled-components";

const PrimaryButton = ({ title = "", onClickCallback = () => {} }) => (
	<Button onClick={onClickCallback}>{title}</Button>
);

const Button = styled.div`
	width: 158px;
	height: 40px;
	background-color: #333;
	border-radius: 3px;
	display: flex;
	justify-content: center;
	border: 1px solid black;
	align-items: center;
	color: white;
	font-family: "Roboto", sans-serif;
	font-size: 18px;

	transition: background-color 0.3s ease;

	:hover {
		background-color: #f37878;
		cursor: pointer;
	}
`;

export default PrimaryButton;
