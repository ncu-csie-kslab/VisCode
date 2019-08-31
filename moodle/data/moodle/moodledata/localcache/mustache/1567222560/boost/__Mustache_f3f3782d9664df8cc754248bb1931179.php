<?php

class __Mustache_f3f3782d9664df8cc754248bb1931179 extends Mustache_Template
{
    private $lambdaHelper;

    public function renderInternal(Mustache_Context $context, $indent = '')
    {
        $this->lambdaHelper = new Mustache_LambdaHelper($this->mustache, $context);
        $buffer = '';

        $buffer .= $indent . '<header id="page-header" class="row">
';
        $buffer .= $indent . '    <div class="col-12 pt-3 pb-3">
';
        $buffer .= $indent . '        <div class="card ';
        // 'contextheader' inverted section
        $value = $context->find('contextheader');
        if (empty($value)) {
            
            $buffer .= 'border-0 bg-transparent';
        }
        $buffer .= '">
';
        $buffer .= $indent . '            <div class="card-body ';
        // 'contextheader' inverted section
        $value = $context->find('contextheader');
        if (empty($value)) {
            
            $buffer .= 'p-2';
        }
        $buffer .= '">
';
        $buffer .= $indent . '                <div class="d-flex">
';
        // 'contextheader' section
        $value = $context->find('contextheader');
        $buffer .= $this->sectionAd1f2cf08e469fbe624aef612f9faf70($context, $indent, $value);
        $buffer .= $indent . '
';
        // 'settingsmenu' section
        $value = $context->find('settingsmenu');
        $buffer .= $this->sectionD23da9ef0f20ebacb8f571607790cf91($context, $indent, $value);
        $buffer .= $indent . '                </div>
';
        $buffer .= $indent . '                <div class="d-flex flex-wrap">
';
        // 'hasnavbar' section
        $value = $context->find('hasnavbar');
        $buffer .= $this->section0cfab5d9b41b9a13eee3763050c03dca($context, $indent, $value);
        $buffer .= $indent . '                    <div class="ml-auto d-flex">
';
        $buffer .= $indent . '                        ';
        $value = $this->resolveValue($context->find('pageheadingbutton'), $context);
        $buffer .= $value;
        $buffer .= '
';
        $buffer .= $indent . '                    </div>
';
        $buffer .= $indent . '                    <div id="course-header">
';
        $buffer .= $indent . '                        ';
        $value = $this->resolveValue($context->find('courseheader'), $context);
        $buffer .= $value;
        $buffer .= '
';
        $buffer .= $indent . '                    </div>
';
        $buffer .= $indent . '                </div>
';
        $buffer .= $indent . '            </div>
';
        $buffer .= $indent . '        </div>
';
        $buffer .= $indent . '    </div>
';
        $buffer .= $indent . '</header>';

        return $buffer;
    }

    private function sectionAd1f2cf08e469fbe624aef612f9faf70(Mustache_Context $context, $indent, $value)
    {
        $buffer = '';
    
        if (!is_string($value) && is_callable($value)) {
            $source = '
                    <div class="mr-auto">
                        {{{contextheader}}}
                    </div>
                    ';
            $result = call_user_func($value, $source, $this->lambdaHelper);
            if (strpos($result, '{{') === false) {
                $buffer .= $result;
            } else {
                $buffer .= $this->mustache
                    ->loadLambda((string) $result)
                    ->renderInternal($context);
            }
        } elseif (!empty($value)) {
            $values = $this->isIterable($value) ? $value : array($value);
            foreach ($values as $value) {
                $context->push($value);
                
                $buffer .= $indent . '                    <div class="mr-auto">
';
                $buffer .= $indent . '                        ';
                $value = $this->resolveValue($context->find('contextheader'), $context);
                $buffer .= $value;
                $buffer .= '
';
                $buffer .= $indent . '                    </div>
';
                $context->pop();
            }
        }
    
        return $buffer;
    }

    private function sectionD23da9ef0f20ebacb8f571607790cf91(Mustache_Context $context, $indent, $value)
    {
        $buffer = '';
    
        if (!is_string($value) && is_callable($value)) {
            $source = '
                    <div class="context-header-settings-menu">
                        {{{settingsmenu}}}
                    </div>
                    ';
            $result = call_user_func($value, $source, $this->lambdaHelper);
            if (strpos($result, '{{') === false) {
                $buffer .= $result;
            } else {
                $buffer .= $this->mustache
                    ->loadLambda((string) $result)
                    ->renderInternal($context);
            }
        } elseif (!empty($value)) {
            $values = $this->isIterable($value) ? $value : array($value);
            foreach ($values as $value) {
                $context->push($value);
                
                $buffer .= $indent . '                    <div class="context-header-settings-menu">
';
                $buffer .= $indent . '                        ';
                $value = $this->resolveValue($context->find('settingsmenu'), $context);
                $buffer .= $value;
                $buffer .= '
';
                $buffer .= $indent . '                    </div>
';
                $context->pop();
            }
        }
    
        return $buffer;
    }

    private function section0cfab5d9b41b9a13eee3763050c03dca(Mustache_Context $context, $indent, $value)
    {
        $buffer = '';
    
        if (!is_string($value) && is_callable($value)) {
            $source = '
                    <div id="page-navbar">
                        {{{navbar}}}
                    </div>
                    ';
            $result = call_user_func($value, $source, $this->lambdaHelper);
            if (strpos($result, '{{') === false) {
                $buffer .= $result;
            } else {
                $buffer .= $this->mustache
                    ->loadLambda((string) $result)
                    ->renderInternal($context);
            }
        } elseif (!empty($value)) {
            $values = $this->isIterable($value) ? $value : array($value);
            foreach ($values as $value) {
                $context->push($value);
                
                $buffer .= $indent . '                    <div id="page-navbar">
';
                $buffer .= $indent . '                        ';
                $value = $this->resolveValue($context->find('navbar'), $context);
                $buffer .= $value;
                $buffer .= '
';
                $buffer .= $indent . '                    </div>
';
                $context->pop();
            }
        }
    
        return $buffer;
    }

}
