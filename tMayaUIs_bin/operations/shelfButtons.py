if (ctrl_l_foot01.footRoll > 0){
	mLoc_l_leftRoll01.rotateZ = ctrl_l_foot01.footRoll * -1 * 30;
	mLoc_l_rightRoll01.rotateZ = 0;
}else if (ctrl_l_foot01.footRoll < 0) {
	mLoc_l_leftRoll01.rotateZ = 0;
	mLoc_l_rightRoll01.rotateZ =  ctrl_l_foot01.footRoll * -1 * 30;
}else {
	mLoc_l_leftRoll01.rotateZ = 0;
	mLoc_l_rightRoll01.rotateZ = 0;
};