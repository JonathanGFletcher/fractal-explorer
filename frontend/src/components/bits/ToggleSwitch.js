import React, { useState, useEffect } from "react";
import styled from "styled-components";

const ToggleSwitch = ({ isToggled = false, onToggle = () => {} }) => {
	return (
		<>
			<Switch>
				<Input
					type="checkbox"
					checked={isToggled}
					onChange={onToggle}
				/>
				<Slider />
			</Switch>
		</>
	);
};

const Switch = styled.label`
	position: relative;
`;

const Input = styled.input`
	position: absolute;
	opacity: 0;
	width: 0;
	height: 0;

	&:checked + span {
		background-color: #f37878;

		&:before {
			left: 33px;
		}
	}
`;

const Slider = styled.span`
	box-sizing: border-box;
	cursor: pointer;
	position: relative;
	display: flex;
	width: 60px;
	height: 30px;
	border-radius: 15px;
	border: 2px solid #333;
	transition: background-color 0.2s ease;

	&:before {
		position: absolute;
		content: "";
		width: 20px;
		height: 20px;
		top: 3px;
		left: 3px;
		border-radius: 10px;
		transition: 0.2s;
		background: #fff;
	}
`;

export default ToggleSwitch;
