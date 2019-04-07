#include "mplist.h"


MPNode operator*(const MPNode& l_node, const MPNode& r_node)
{
	MPNode retNode;
	if (l_node.elem_tag == COEF && r_node.elem_tag == COEF)
	{
		retNode.elem_tag = COEF;
		retNode.coef = l_node.coef * r_node.coef;
	}
	else if (l_node.elem_tag == LIST && r_node.elem_tag == LIST)
	{
		retNode.elem_tag = LIST;
		retNode.list_ptr = (*l_node.list_ptr) * (*r_node.list_ptr);
	}
	else if (l_node.elem_tag == COEF)
	{
		retNode.elem_tag = LIST;
		retNode.list_ptr = (*r_node.list_ptr) * l_node.coef;
	}
	else // if (l_node.elem_tag == COEF)
	{
		retNode.elem_tag = LIST;
		retNode.list_ptr = (*l_node.list_ptr) * r_node.coef;
	}
	// 指数位相加
	retNode.exp = l_node.exp + r_node.exp;
	return retNode;
}

MPNode _NodeMulti(const MPNode& node, float num)
{
	MPNode retNode;
	if (node.elem_tag == COEF)
	{
		retNode.elem_tag = COEF;
		retNode.coef = node.coef * num;
	}
	else // if (node.elem_tag == LIST)
	{
		retNode.elem_tag = LIST;
		retNode.list_ptr = (*node.list_ptr) * num;
	}
	// 指数位不动
	retNode.exp = node.exp;
	return retNode;
}

MPNode operator*(const MPNode& node, float num)
{
	return _NodeMulti(node, num);
}

MPNode operator*(float num, const MPNode& node)
{
	return _NodeMulti(node, num);
}

MPNode* MPNode::operator+=(const MPNode& node)
{
	if (node.exp != this->exp)
		return nullptr;
	 
	if (node.elem_tag == COEF && elem_tag == COEF)
	{
		coef += node.coef;
	}
	else if(node.elem_tag == LIST && elem_tag == LIST)
	{

	}
	return this;
}
