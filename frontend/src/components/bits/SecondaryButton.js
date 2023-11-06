import React from "react";
import styled from "styled-components";

const SecondaryButton = ({ title = "", onClickCallback = () => {} }) => (
	<Button onClick={onClickCallback}>{title}</Button>
);

const Button = styled.div`
	width: 158px;
	height: 40px;
	background-color: #eee;
	border-radius: 3px;
	display: flex;
	justify-content: center;
	border: 1px solid black;
	align-items: center;
	font-family: "Roboto", sans-serif;
	font-size: 18px;

	transition: background-color 0.3s ease, border 1s ease, color 0.3s ease;

	:hover {
		background-color: #f37878;
		color: white;
		cursor: pointer;
		border: 1px solid #f37878;
	}
`;

export default SecondaryButton;
