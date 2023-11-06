import React, { useState, useEffect } from "react";
import styled from "styled-components";

const App = () => {
	// Data
	// const [user, setUser] = useState(null);

	// Site
	// const [selectedPage, setSelectedPage] = useState("Home");

	// Get user data from server
	// useEffect(() => {
	// 	fetch("/api")
	// 		.then((res) => (res.status === 200 ? res.json() : { user: false }))
	// 		.then((json) => {
	// 			setUser(json?.user ?? null);
	// 		})
	// 		.catch((e) => alert(e));
	// }, []);

	return (
		<>
			<Background>
				
			</Background>
		</>
	);
};

const Background = styled.div`
	background-color: #222222;
	width: 100vw;
	height: 100vh;
`;

export default App;
