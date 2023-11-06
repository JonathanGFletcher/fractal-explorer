import React from "react";
import styled from "styled-components";

const NavButton = ({
	title = "",
	icon = <></>,
	selected = false,
	onClickCallback = () => {},
}) => {
	return (
		<>
			<Container>
				<Background
					onClick={() => onClickCallback(title)}
					style={{ border: selected ? "1px solid #F37878" : "" }}
				>
					{icon}
					<Title>{title}</Title>
				</Background>
			</Container>
		</>
	);
};

const Container = styled.div`
	width: 100%;
	height: 60px;
	display: flex;
	justify-content: center;
	align-items: center;
`;

const Background = styled.div`
	width: 90%;
	height: 50px;
	background-color: #434343;
	border-radius: 5px;
	display: flex;
	align-items: center;
	padding-left: 10px;
	transition: background-color 0.3s ease;

	:hover {
		background-color: #f37878;
		color: white;
		cursor: pointer;
	}
`;

const Title = styled.div`
	color: white;
	font-family: "Roboto", sans-serif;
	padding-left: 10px;
`;

export default NavButton;
