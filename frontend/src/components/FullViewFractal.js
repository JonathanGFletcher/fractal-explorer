import React, { useState, useEffect } from "react";
import { useFractalContext, useFractalUpdateContext } from "../contexts/FractalContext";
import styled from "styled-components";
import * as NetworkService from "../services/NetworkService";
import InputField from "./bits/InputField";
import PrimaryButton from "./bits/PrimaryButton";
import SecondaryButton from "./bits/SecondaryButton";
import { DEFAULT_FULL_VIEW_PARAMS } from "../Constants";

const FullViewFractal = () => {

    const FractalContext = useFractalContext();
    const params = FractalContext?.fullViewParams;

    const FractalUpdateContext = useFractalUpdateContext();
    const updateFullViewParams = FractalUpdateContext?.updateFullViewParams;

    const tilesX = 5;
    const tilesY = 4;

    const { innerWidth, innerHeight } = window;
    const fullImageWidth = innerWidth - 20;
    const fullImageHeight = innerHeight - 20;
    const chunkWidth = fullImageWidth / tilesX;
    const chunkHeight = fullImageHeight / tilesY;

    const tiles = Array.from(
        Array(tilesX), (_, x) => 
            Array.from(
                Array(tilesY), (_, y) => {
                    return {
                        x: x,
                        y: y,
                    }
                }
            )
    );

    const [showParamsPanel, setShowParamsPanel] = useState(true);

    return <Container>
        <FractalContainer>

            { tiles.map(row => 
                <FractalRow>

                    { row.map(c => 
                        <FractalChunk>
                            <FractalImage 
                            x={ c.x } y={ c.y } 
                            tilesX={ tilesX } tilesY={ tilesY } 
                            chunkWidth={ chunkWidth } chunkHeight={ chunkHeight } 
                            params={ params } 
                            />
                        </FractalChunk>
                    ) }

                </FractalRow>
            ) }
            
        </FractalContainer>
        <ParamsPanel show={ showParamsPanel } params={ params } setParams={ updateFullViewParams } />
    </Container>
}

const Container = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    padding: 10px;
`;

const FractalContainer = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
`;

const FractalRow = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
`;

const FractalChunk = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
`;



const FractalImage = ({ x, y, tilesX, tilesY, chunkWidth, chunkHeight, params }) => {
    if (params == null) {
        return <FractalBackground>
            <FractalBackgroundPlaceholder />
        </FractalBackground>
    }

    const width = params?.dimensions?.width / tilesX;
    const height = params?.dimensions?.height / tilesY;

    const minX = width * x;
    const minY = height * y;
    const maxX = width * x + width - 1;
    const maxY = height * y + height - 1;

    const reqParams = {
        ...params,
        dimensions: {
            ...params?.dimensions,
            view_min_x: minX,
            view_min_y: minY,
            view_max_x: maxX,
            view_max_y: maxY,
        }
    };

    const [imageUrl, setImageUrl] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        setImageUrl(null);
        setError(null);
        
        NetworkService.getFractal(reqParams)
        .then(data => setImageUrl(data?.url))
        .then(() => setError(null))
        .catch(e => setError(e));
    }, [params]);

    return <FractalImageContainer>
        { imageUrl == null || error ?
            <FractalBackground>
                <FractalBackgroundPlaceholder style={{ backgroundColor: error ? '#8c0000' : '#262626' }} />
            </FractalBackground>
            :
            <img src={ imageUrl } style={{ position: 'relative', width: chunkWidth, height: chunkHeight }} />
        }
    </FractalImageContainer>
}

const FractalImageContainer = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    overflow: hidden;
`;

const FractalBackground = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    padding: 5px;
`;

const FractalBackgroundPlaceholder = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    background-color: #262626;
    border-radius: 5px;
`;



const ParamsPanel = ({ show, params, setParams }) => {
    if (!show) return <></>

    const [currentConstantX, setCurrentConstantX] = useState(params?.constant?.x);
    const [currentConstantY, setCurrentConstantY] = useState(params?.constant?.y);
    const [currentIterations, setCurrentIterations] = useState(params?.iterations);
    const [currentCenterX, setCurrentCenterX] = useState(params?.center?.x);
    const [currentCenterY, setCurrentCenterY] = useState(params?.center?.y);
    const [currentScale, setCurrentScale] = useState(params?.scale);
    const [currentWidth, setCurrentWidth] = useState(params?.dimensions?.width);
    const [currentHeight, setCurrentHeight] = useState(params?.dimensions?.height);
    const [currentSamples, setCurrentSamples] = useState(params?.samples);

    const resetToCurrentState = () => {
        setCurrentConstantX(params?.constant?.x);
        setCurrentConstantY(params?.constant?.y);
        setCurrentIterations(params?.iterations);
        setCurrentCenterX(params?.center?.x);
        setCurrentCenterY(params?.center?.y);
        setCurrentScale(params?.scale);
        setCurrentWidth(params?.dimensions?.width);
        setCurrentHeight(params?.dimensions?.height);
        setCurrentSamples(params?.samples);
    }

    const updateFractal = () => {
        const newParams = {
            ...params,
            constant: {
                x: currentConstantX === "" ? DEFAULT_FULL_VIEW_PARAMS["constant_x"] : Number(currentConstantX),
                y: currentConstantY === "" ? DEFAULT_FULL_VIEW_PARAMS["constant_y"] : Number(currentConstantY),
            },
            center: {
                x: currentCenterX === "" ? DEFAULT_FULL_VIEW_PARAMS["center_x"] : Number(currentCenterX),
                y: currentCenterY === "" ? DEFAULT_FULL_VIEW_PARAMS["center_y"] : Number(currentCenterY),
            },
            scale: currentScale === "" ? DEFAULT_FULL_VIEW_PARAMS["scale"] : Number(currentScale),
            iterations: currentIterations === "" ? DEFAULT_FULL_VIEW_PARAMS["iterations"] : Number(currentIterations),
            samples: currentSamples === "" ? DEFAULT_FULL_VIEW_PARAMS["samples"] : Number(currentSamples),
            dimensions: {
                width: currentWidth === "" ? DEFAULT_FULL_VIEW_PARAMS["dimensions"]["width"] : Number(currentWidth),
                height: currentHeight === "" ? DEFAULT_FULL_VIEW_PARAMS["dimensions"]["height"] : Number(currentHeight),
            },
        };

        setCurrentConstantX(newParams?.constant?.x);
        setCurrentConstantY(newParams?.constant?.y);
        setCurrentIterations(newParams?.iterations);
        setCurrentCenterX(newParams?.center?.x);
        setCurrentCenterY(newParams?.center?.y);
        setCurrentScale(newParams?.scale);
        setCurrentWidth(newParams?.dimensions?.width);
        setCurrentHeight(newParams?.dimensions?.height);
        setCurrentSamples(newParams?.samples);

        setParams(newParams);
    }

    return <ParamsPanelContainer>
        <ParamsPanelForm>

            <ParamsPanelSectionLabel>Fractal</ParamsPanelSectionLabel>

            <ParamsPanelLabel>Constant</ParamsPanelLabel>
            <ParamsPanelHStack>
                <ParamsPanelHStackSection>
                    <InputField 
                    inputType="number" 
                    placeholder={`${DEFAULT_FULL_VIEW_PARAMS["constant_x"]}`} 
                    defaultValue={currentConstantX}
                    onChangeCallback={ e => setCurrentConstantX(e.target.value) }
                    />
                </ParamsPanelHStackSection>
                <ParamsPanelHStackSection>
                    <InputField 
                    inputType="number" 
                    placeholder={`${DEFAULT_FULL_VIEW_PARAMS["constant_y"]}`} 
                    defaultValue={currentConstantY}
                    onChangeCallback={ e => setCurrentConstantY(e.target.value) }
                    />
                </ParamsPanelHStackSection>
            </ParamsPanelHStack>

            <ParamsPanelLabel>Iterations</ParamsPanelLabel>
            <ParamsPanelHStack>
                <ParamsPanelHStackSection>
                    <InputField 
                    inputType="number" 
                    placeholder={`${DEFAULT_FULL_VIEW_PARAMS["iterations"]}`} 
                    defaultValue={currentIterations}
                    onChangeCallback={ e => setCurrentIterations(e.target.value) }
                    />
                </ParamsPanelHStackSection>
                <ParamsPanelHStackSection />
            </ParamsPanelHStack>

            <ParamsPanelPadding />
            <ParamsPanelSectionLabel>Scope</ParamsPanelSectionLabel>

            <ParamsPanelLabel>Center</ParamsPanelLabel>
            <ParamsPanelHStack>
                <ParamsPanelHStackSection>
                    <InputField 
                    inputType="number" 
                    placeholder={`${DEFAULT_FULL_VIEW_PARAMS["center_x"]}`} 
                    defaultValue={currentCenterX}
                    onChangeCallback={ e => setCurrentCenterX(e.target.value) }
                    />
                </ParamsPanelHStackSection>
                <ParamsPanelHStackSection>
                    <InputField 
                    inputType="number" 
                    placeholder={`${DEFAULT_FULL_VIEW_PARAMS["center_y"]}`} 
                    defaultValue={currentCenterY}
                    onChangeCallback={ e => setCurrentCenterY(e.target.value) }
                    />
                </ParamsPanelHStackSection>
            </ParamsPanelHStack>

            <ParamsPanelLabel>Scale</ParamsPanelLabel>
            <ParamsPanelHStack>
                <ParamsPanelHStackSection>
                    <InputField 
                    inputType="number" 
                    placeholder={`${DEFAULT_FULL_VIEW_PARAMS["scale"]}`}
                    defaultValue={currentScale} 
                    onChangeCallback={ e => setCurrentScale(e.target.value) }
                    />
                </ParamsPanelHStackSection>
                <ParamsPanelHStackSection />
            </ParamsPanelHStack>

            <ParamsPanelPadding />
            <ParamsPanelSectionLabel>Quality</ParamsPanelSectionLabel>

            <ParamsPanelLabel>Render Size { " ( Width / Height )" }</ParamsPanelLabel>
            <ParamsPanelHStack>
                <ParamsPanelHStackSection>
                    <InputField 
                    inputType="number" 
                    placeholder={`${DEFAULT_FULL_VIEW_PARAMS["dimensions"]["width"]}`} 
                    defaultValue={currentWidth}
                    onChangeCallback={ e => setCurrentWidth(e.target.value) }
                    />
                </ParamsPanelHStackSection>
                <ParamsPanelHStackSection>
                    <InputField 
                    inputType="number" 
                    placeholder={`${DEFAULT_FULL_VIEW_PARAMS["dimensions"]["height"]}`} 
                    defaultValue={currentHeight}
                    onChangeCallback={ e => setCurrentHeight(e.target.value) }
                    />
                </ParamsPanelHStackSection>
            </ParamsPanelHStack>

            <ParamsPanelLabel>Samples</ParamsPanelLabel>
            <ParamsPanelHStack>
                <ParamsPanelHStackSection>
                    <InputField 
                    inputType="number" 
                    placeholder={`${DEFAULT_FULL_VIEW_PARAMS["samples"]}`} 
                    defaultValue={currentSamples}
                    onChangeCallback={ e => setCurrentSamples(e.target.value) }
                    />
                </ParamsPanelHStackSection>
                <ParamsPanelHStackSection />
            </ParamsPanelHStack>

            <ParamsPanelPadding />

            <ParamsPanelButtonSection>
                <PrimaryButton title="Reset" onClickCallback={ resetToCurrentState }/>
            </ParamsPanelButtonSection>

            <ParamsPanelButtonSection>
                <SecondaryButton title="Render" onClickCallback={ updateFractal } />
            </ParamsPanelButtonSection>

        </ParamsPanelForm>
    </ParamsPanelContainer>
}

const ParamsPanelContainer = styled.div`
    position: absolute;
    z-index: 9;
    float: right;
    top: 20px;
    right: 20px;
    width: 300px;
    height: auto;
    border-radius: 5px;
    background-color: #212121;
    box-shadow: 0px 0px 20px black;
    padding: 10px;
    opacity: 0.85;
`;

const ParamsPanelForm = styled.div`
    position: relative;
    width: 100%;
    height: auto;
`;

const ParamsPanelSectionLabel = styled.div`
    position: relative;
    font-size: 15px;
	font-family: "Roboto", sans-serif;
    color: #EEE;
    border-bottom: 1px solid #EEE;
    margin-bottom: 20px;
`;

const ParamsPanelLabel = styled.div`
    position: relative;
    font-size: 15px;
	font-family: "Roboto", sans-serif;
    color: #BBB;
`;

const ParamsPanelHStack = styled.div`
    position: relative;
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: row;
`;

const ParamsPanelHStackSection = styled.div`
    position: relative;
    padding: 5px;
    width: 100%;
    height: auto;
`;

const ParamsPanelButtonSection = styled.div`
    position: relative;
    width: 100%;
    height: auto;
    display: flex;
    justify-content: center;
    align-items: center;
`;

const ParamsPanelPadding = styled.div`
    position: relative;
    width: 100%;
    height: 30px;
`;


export default FullViewFractal;